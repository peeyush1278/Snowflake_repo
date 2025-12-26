"""
ImpactGuard AI - Streamlit Application
A Data Quality Monitor and 4-Week Demand Forecast Tool for Health and Education Programs

Author: Senior Snowflake Engineer
Version: 1.0
Theme: AI for Good
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import json

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ImpactGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1E88E5 0%, #43A047 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        color: #856404;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION INITIALIZATION
# ============================================================================

# Get Snowflake session
session = get_active_session()

# Initialize session state
if 'configured' not in st.session_state:
    st.session_state.configured = False
if 'database' not in st.session_state:
    st.session_state.database = None
if 'schema' not in st.session_state:
    st.session_state.schema = None
if 'table' not in st.session_state:
    st.session_state.table = None
if 'date_column' not in st.session_state:
    st.session_state.date_column = None
if 'value_column' not in st.session_state:
    st.session_state.value_column = None
if 'category_column' not in st.session_state:
    st.session_state.category_column = None

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="main-header">🛡️ ImpactGuard AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Data Quality Monitor & 4-Week Demand Forecast for Social Impact Programs</p>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    # Database Selection
    st.subheader("1. Select Data Source")
    
    try:
        # Get available databases
        databases_df = session.sql("SHOW DATABASES").collect()
        databases = [row['name'] for row in databases_df]
        
        selected_db = st.selectbox(
            "Database",
            options=databases,
            index=databases.index(st.session_state.database) if st.session_state.database in databases else 0,
            key="db_select"
        )
        
        # Get schemas in selected database
        schemas_df = session.sql(f"SHOW SCHEMAS IN DATABASE {selected_db}").collect()
        schemas = [row['name'] for row in schemas_df]
        
        selected_schema = st.selectbox(
            "Schema",
            options=schemas,
            index=schemas.index(st.session_state.schema) if st.session_state.schema in schemas else 0,
            key="schema_select"
        )
        
        # Get tables in selected schema
        tables_df = session.sql(f"SHOW TABLES IN SCHEMA {selected_db}.{selected_schema}").collect()
        tables = [row['name'] for row in tables_df]
        
        selected_table = st.selectbox(
            "Table",
            options=tables,
            index=tables.index(st.session_state.table) if st.session_state.table in tables else 0,
            key="table_select"
        )
        
        st.markdown("---")
        
        # Column Mapping
        st.subheader("2. Map Your Columns")
        
        # Get columns from selected table
        full_table_name = f"{selected_db}.{selected_schema}.{selected_table}"
        columns_df = session.table(full_table_name).limit(1).to_pandas()
        columns = list(columns_df.columns)
        
        date_col = st.selectbox(
            "📅 Date Column",
            options=columns,
            index=columns.index(st.session_state.date_column) if st.session_state.date_column in columns else 0,
            help="Column containing date/timestamp values"
        )
        
        value_col = st.selectbox(
            "📊 Value/Metric Column",
            options=columns,
            index=columns.index(st.session_state.value_column) if st.session_state.value_column in columns else 0,
            help="Column containing numeric values to analyze"
        )
        
        category_col = st.selectbox(
            "🏷️ Category Column (Optional)",
            options=["None"] + columns,
            index=columns.index(st.session_state.category_column) if st.session_state.category_column in columns else 0,
            help="Column for grouping data (e.g., program type, region)"
        )
        
        category_col = None if category_col == "None" else category_col
        
        st.markdown("---")
        
        # Save Configuration Button
        if st.button("💾 Save Configuration", type="primary", use_container_width=True):
            st.session_state.database = selected_db
            st.session_state.schema = selected_schema
            st.session_state.table = selected_table
            st.session_state.date_column = date_col
            st.session_state.value_column = value_col
            st.session_state.category_column = category_col
            st.session_state.configured = True
            st.success("✅ Configuration saved!")
            st.rerun()
        
        # Display current configuration
        if st.session_state.configured:
            st.markdown("---")
            st.success("✅ Configuration Active")
            with st.expander("View Current Config"):
                st.write(f"**Table:** `{st.session_state.database}.{st.session_state.schema}.{st.session_state.table}`")
                st.write(f"**Date:** `{st.session_state.date_column}`")
                st.write(f"**Value:** `{st.session_state.value_column}`")
                st.write(f"**Category:** `{st.session_state.category_column or 'None'}`")
    
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

if not st.session_state.configured:
    st.info("👈 Please configure your data source in the sidebar to get started.")
    
    # Welcome message
    st.markdown("## Welcome to ImpactGuard AI!")
    st.markdown("""
    This tool helps program managers in **Health** and **Education** sectors to:
    
    - 🔍 **Monitor Data Quality**: Detect nulls, duplicates, and outliers automatically
    - 📈 **Forecast Demand**: Generate 4-week predictions for resource planning
    - 🤖 **Get AI Insights**: Receive actionable recommendations powered by Snowflake Cortex
    
    ### Getting Started
    1. Select your database, schema, and table from the sidebar
    2. Map your columns (Date, Value, Category)
    3. Click "Save Configuration"
    4. Explore the Data Quality, Forecast, and AI Insights tabs
    
    **Built with ❤️ for Social Impact**
    """)

else:
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Data Quality", "📈 Forecast", "🤖 AI Insights"])
    
    # ========================================================================
    # TAB 1: DATA QUALITY
    # ========================================================================
    
    with tab1:
        st.header("Data Quality Analysis")
        st.markdown("Comprehensive checks for data integrity and reliability")
        
        if st.button("🔍 Run Quality Check", type="primary"):
            with st.spinner("Analyzing data quality..."):
                try:
                    # Call stored procedure
                    result = session.call(
                        'app_schema.check_data_quality',
                        st.session_state.database,
                        st.session_state.schema,
                        st.session_state.table,
                        st.session_state.value_column,
                        st.session_state.date_column,
                        st.session_state.category_column or ''
                    )
                    
                    # Parse result
                    if isinstance(result, str):
                        result = json.loads(result)
                    
                    # Display Quality Score
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        score = result['quality_score']
                        color = "#43A047" if score >= 80 else "#FB8C00" if score >= 60 else "#E53935"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <h2 style="color: {color}; margin: 0;">Data Quality Score</h2>
                            <h1 style="color: {color}; margin: 0.5rem 0;">{score}/100</h1>
                            <p style="margin: 0;">{'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Needs Attention'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Total Rows", f"{result['total_rows']:,}")
                    
                    with col3:
                        st.metric("Duplicates", result['duplicate_count'])
                    
                    st.markdown("---")
                    
                    # Null Values Analysis
                    st.subheader("📊 Null Values Analysis")
                    null_data = result['null_counts']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        null_pct = (null_data['value_nulls'] / result['total_rows']) * 100
                        st.metric(
                            "Value Column Nulls",
                            null_data['value_nulls'],
                            f"{null_pct:.2f}%"
                        )
                    with col2:
                        null_pct = (null_data['date_nulls'] / result['total_rows']) * 100
                        st.metric(
                            "Date Column Nulls",
                            null_data['date_nulls'],
                            f"{null_pct:.2f}%"
                        )
                    with col3:
                        null_pct = (null_data.get('category_nulls', 0) / result['total_rows']) * 100
                        st.metric(
                            "Category Column Nulls",
                            null_data.get('category_nulls', 0),
                            f"{null_pct:.2f}%"
                        )
                    
                    # Outliers Analysis
                    st.subheader("🎯 Outlier Detection")
                    outlier_count = result['outlier_count']
                    outlier_pct = (outlier_count / result['total_rows']) * 100
                    
                    if outlier_count > 0:
                        st.warning(f"⚠️ Found {outlier_count} outliers ({outlier_pct:.2f}% of data)")
                        if result.get('outlier_indices'):
                            st.info(f"Sample outlier row indices: {', '.join(map(str, result['outlier_indices'][:5]))}")
                    else:
                        st.success("✅ No outliers detected!")
                    
                    # Recommendations
                    st.markdown("---")
                    st.subheader("💡 Recommendations")
                    
                    if score >= 80:
                        st.markdown('<div class="success-box">✅ Your data quality is excellent! No immediate action required.</div>', unsafe_allow_html=True)
                    elif score >= 60:
                        st.markdown('<div class="warning-box">⚠️ Consider addressing null values and duplicates to improve data quality.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-box">❌ Data quality needs attention. Review null values, duplicates, and outliers.</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error running quality check: {str(e)}")
    
    # ========================================================================
    # TAB 2: FORECAST
    # ========================================================================
    
    with tab2:
        st.header("4-Week Demand Forecast")
        st.markdown("Predictive analytics for resource planning and decision-making")
        
        if st.button("📈 Generate Forecast", type="primary"):
            with st.spinner("Generating 4-week forecast..."):
                try:
                    # Call stored procedure
                    result = session.call(
                        'app_schema.generate_forecast',
                        st.session_state.database,
                        st.session_state.schema,
                        st.session_state.table,
                        st.session_state.value_column,
                        st.session_state.date_column,
                        st.session_state.category_column or ''
                    )
                    
                    # Parse result
                    if isinstance(result, str):
                        result = json.loads(result)
                    
                    if result['status'] == 'error':
                        st.error(result['message'])
                    else:
                        # Display model metrics
                        st.subheader("📊 Model Performance")
                        col1, col2, col3 = st.columns(3)
                        
                        metrics = result['model_metrics']
                        with col1:
                            st.metric("R² Score", f"{metrics['r_squared']:.4f}")
                        with col2:
                            st.metric("Trend Coefficient", f"{metrics['coefficient']:.4f}")
                        with col3:
                            st.metric("Intercept", f"{metrics['intercept']:.2f}")
                        
                        st.markdown("---")
                        
                        # Visualization
                        st.subheader("📈 Forecast Visualization")
                        
                        # Prepare data for plotting
                        historical = result['historical']
                        forecast = result['forecast']
                        
                        # Create figure
                        fig = go.Figure()
                        
                        # Historical data
                        fig.add_trace(go.Scatter(
                            x=historical['dates'],
                            y=historical['values'],
                            mode='lines+markers',
                            name='Historical Data',
                            line=dict(color='#1E88E5', width=2),
                            marker=dict(size=6)
                        ))
                        
                        # Forecast data
                        fig.add_trace(go.Scatter(
                            x=forecast['dates'],
                            y=forecast['values'],
                            mode='lines+markers',
                            name='4-Week Forecast',
                            line=dict(color='#43A047', width=2, dash='dash'),
                            marker=dict(size=6, symbol='diamond')
                        ))
                        
                        # Update layout
                        fig.update_layout(
                            title='Historical Data & 4-Week Forecast',
                            xaxis_title='Date',
                            yaxis_title=st.session_state.value_column,
                            hovermode='x unified',
                            height=500,
                            template='plotly_white'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Forecast table
                        st.subheader("📋 Forecast Details")
                        forecast_df = pd.DataFrame({
                            'Date': forecast['dates'],
                            'Predicted Value': [f"{v:.2f}" for v in forecast['values']]
                        })
                        st.dataframe(forecast_df, use_container_width=True, hide_index=True)
                        
                        # Download forecast
                        csv = forecast_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Forecast CSV",
                            data=csv,
                            file_name="impactguard_forecast.csv",
                            mime="text/csv"
                        )
                
                except Exception as e:
                    st.error(f"Error generating forecast: {str(e)}")
    
    # ========================================================================
    # TAB 3: AI INSIGHTS
    # ========================================================================
    
    with tab3:
        st.header("AI-Powered Insights")
        st.markdown("Actionable recommendations powered by Snowflake Cortex AI")
        
        if st.button("🤖 Generate AI Insights", type="primary"):
            with st.spinner("Analyzing data and generating insights..."):
                try:
                    # Get data summary
                    full_table_name = f"{st.session_state.database}.{st.session_state.schema}.{st.session_state.table}"
                    df = session.table(full_table_name).to_pandas()
                    
                    # Calculate statistics
                    total_rows = len(df)
                    avg_value = df[st.session_state.value_column].mean()
                    max_value = df[st.session_state.value_column].max()
                    min_value = df[st.session_state.value_column].min()
                    null_count = df[st.session_state.value_column].isna().sum()
                    
                    # Create prompt for Cortex AI
                    prompt = f"""
You are an AI assistant helping program managers in health and education sectors. 
Analyze the following data summary and provide exactly 3 actionable bullet points for improving program outcomes.

Data Summary:
- Total Records: {total_rows}
- Metric: {st.session_state.value_column}
- Average Value: {avg_value:.2f}
- Maximum Value: {max_value:.2f}
- Minimum Value: {min_value:.2f}
- Missing Values: {null_count}

Focus on:
1. Data quality improvements
2. Resource allocation recommendations
3. Trend-based action items

Provide exactly 3 bullet points, each starting with a relevant emoji and action verb.
"""
                    
                    # Call Snowflake Cortex
                    cortex_query = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        'mistral-large',
                        '{prompt.replace("'", "''")}'
                    ) AS insights
                    """
                    
                    insights_result = session.sql(cortex_query).collect()
                    insights_text = insights_result[0]['INSIGHTS']
                    
                    # Display insights
                    st.subheader("💡 AI-Generated Action Plan")
                    st.markdown(insights_text)
                    
                    st.markdown("---")
                    
                    # Display data summary
                    st.subheader("📊 Data Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Records", f"{total_rows:,}")
                    with col2:
                        st.metric("Average Value", f"{avg_value:.2f}")
                    with col3:
                        st.metric("Max Value", f"{max_value:.2f}")
                    with col4:
                        st.metric("Missing Values", null_count)
                    
                    # Distribution chart
                    st.subheader("📈 Value Distribution")
                    fig = px.histogram(
                        df,
                        x=st.session_state.value_column,
                        nbins=30,
                        title=f"Distribution of {st.session_state.value_column}",
                        color_discrete_sequence=['#1E88E5']
                    )
                    fig.update_layout(
                        showlegend=False,
                        height=400,
                        template='plotly_white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error generating AI insights: {str(e)}")
                    st.info("💡 Tip: Ensure Snowflake Cortex is enabled in your account and you have the necessary privileges.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>ImpactGuard AI</strong> v1.0 | Built with ❤️ for Social Impact</p>
    <p>Powered by Snowflake Native App Framework, Streamlit, Snowpark, and Cortex AI</p>
</div>
""", unsafe_allow_html=True)
