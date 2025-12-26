-- ============================================================================
-- ImpactGuard AI - Setup Script
-- Description: Creates application roles, schemas, and objects
-- Version: 1.0
-- ============================================================================

-- Create application role
CREATE APPLICATION ROLE IF NOT EXISTS app_public;

-- Create versioned schema for application objects
CREATE OR ALTER VERSIONED SCHEMA app_schema;

-- Grant usage on schema to application role
GRANT USAGE ON SCHEMA app_schema TO APPLICATION ROLE app_public;

-- ============================================================================
-- STORED PROCEDURES
-- ============================================================================

-- Procedure: Data Quality Check
CREATE OR REPLACE PROCEDURE app_schema.check_data_quality(
    database_name STRING,
    schema_name STRING,
    table_name STRING,
    value_column STRING,
    date_column STRING,
    category_column STRING
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy')
HANDLER = 'run_quality_check'
AS
$$
import pandas as pd
import numpy as np
from snowflake.snowpark import Session

def run_quality_check(session: Session, database_name: str, schema_name: str, 
                      table_name: str, value_column: str, date_column: str, 
                      category_column: str):
    """
    Performs comprehensive data quality checks on the specified table.
    Returns: Dictionary with quality metrics
    """
    
    # Build fully qualified table name
    full_table_name = f"{database_name}.{schema_name}.{table_name}"
    
    # Read data
    df = session.table(full_table_name).to_pandas()
    
    total_rows = len(df)
    
    # Check for nulls
    null_counts = {
        'value_nulls': df[value_column].isna().sum() if value_column in df.columns else 0,
        'date_nulls': df[date_column].isna().sum() if date_column in df.columns else 0,
        'category_nulls': df[category_column].isna().sum() if category_column and category_column in df.columns else 0
    }
    
    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    
    # Outlier detection using IQR method
    outliers = 0
    outlier_indices = []
    if value_column in df.columns and pd.api.types.is_numeric_dtype(df[value_column]):
        Q1 = df[value_column].quantile(0.25)
        Q3 = df[value_column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outlier_mask = (df[value_column] < lower_bound) | (df[value_column] > upper_bound)
        outliers = outlier_mask.sum()
        outlier_indices = df[outlier_mask].index.tolist()[:10]  # Return first 10
    
    # Calculate data quality score (0-100)
    null_penalty = (sum(null_counts.values()) / (total_rows * 3)) * 30
    duplicate_penalty = (duplicate_count / total_rows) * 30
    outlier_penalty = (outliers / total_rows) * 40
    quality_score = max(0, 100 - null_penalty - duplicate_penalty - outlier_penalty)
    
    return {
        'total_rows': int(total_rows),
        'null_counts': null_counts,
        'duplicate_count': int(duplicate_count),
        'outlier_count': int(outliers),
        'outlier_indices': outlier_indices,
        'quality_score': round(quality_score, 2),
        'status': 'success'
    }
$$;

-- Procedure: Generate 4-Week Forecast
CREATE OR REPLACE PROCEDURE app_schema.generate_forecast(
    database_name STRING,
    schema_name STRING,
    table_name STRING,
    value_column STRING,
    date_column STRING,
    category_column STRING
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy', 'scikit-learn', 'snowflake-ml-python')
HANDLER = 'run_forecast'
AS
$$
import pandas as pd
import numpy as np
from datetime import timedelta
from snowflake.snowpark import Session
from sklearn.linear_model import LinearRegression

def run_forecast(session: Session, database_name: str, schema_name: str, 
                 table_name: str, value_column: str, date_column: str, 
                 category_column: str):
    """
    Generates a 4-week demand forecast using linear regression.
    Returns: Dictionary with forecast results
    """
    
    # Build fully qualified table name
    full_table_name = f"{database_name}.{schema_name}.{table_name}"
    
    # Read data
    df = session.table(full_table_name).to_pandas()
    
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Sort by date
    df = df.sort_values(date_column)
    
    # Prepare data for modeling
    df['days_since_start'] = (df[date_column] - df[date_column].min()).dt.days
    
    # Remove nulls
    df_clean = df[[value_column, 'days_since_start']].dropna()
    
    if len(df_clean) < 7:
        return {
            'status': 'error',
            'message': 'Insufficient data for forecasting (minimum 7 records required)'
        }
    
    # Train linear regression model
    X = df_clean[['days_since_start']].values
    y = df_clean[value_column].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate 4-week forecast (28 days)
    last_date = df[date_column].max()
    last_day = df_clean['days_since_start'].max()
    
    forecast_dates = []
    forecast_values = []
    
    for i in range(1, 29):  # 28 days
        future_day = last_day + i
        future_date = last_date + timedelta(days=i)
        predicted_value = model.predict([[future_day]])[0]
        
        forecast_dates.append(future_date.strftime('%Y-%m-%d'))
        forecast_values.append(float(predicted_value))
    
    # Calculate model metrics
    r_squared = model.score(X, y)
    
    # Historical data for visualization
    historical_dates = df[date_column].tail(30).dt.strftime('%Y-%m-%d').tolist()
    historical_values = df[value_column].tail(30).tolist()
    
    return {
        'status': 'success',
        'forecast': {
            'dates': forecast_dates,
            'values': forecast_values
        },
        'historical': {
            'dates': historical_dates,
            'values': historical_values
        },
        'model_metrics': {
            'r_squared': round(r_squared, 4),
            'coefficient': round(float(model.coef_[0]), 4),
            'intercept': round(float(model.intercept_), 4)
        }
    }
$$;

-- Grant execute permissions on procedures
GRANT USAGE ON PROCEDURE app_schema.check_data_quality(STRING, STRING, STRING, STRING, STRING, STRING) 
    TO APPLICATION ROLE app_public;
GRANT USAGE ON PROCEDURE app_schema.generate_forecast(STRING, STRING, STRING, STRING, STRING, STRING) 
    TO APPLICATION ROLE app_public;

-- ============================================================================
-- STREAMLIT APPLICATION
-- ============================================================================

CREATE OR REPLACE STREAMLIT app_schema.impactguard_ui
FROM '/streamlit'
MAIN_FILE = '/app.py'
COMMENT = 'ImpactGuard AI - Data Quality Monitor and Demand Forecast Tool';

-- Grant usage on Streamlit to application role
GRANT USAGE ON STREAMLIT app_schema.impactguard_ui TO APPLICATION ROLE app_public;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

-- Log successful setup
SELECT 'ImpactGuard AI setup completed successfully!' AS setup_status;
