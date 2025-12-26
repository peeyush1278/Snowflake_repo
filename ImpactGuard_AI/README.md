# ImpactGuard AI 🛡️

**A Snowflake Native App for Data Quality Monitoring and Demand Forecasting**

Built for Health and Education program managers who need powerful analytics without the complexity.

---

## 🎯 Overview

ImpactGuard AI is a reusable, plug-and-play Snowflake Native App that empowers non-technical program managers to:

- **Monitor Data Quality**: Automatically detect nulls, duplicates, and outliers
- **Forecast Demand**: Generate 4-week predictions for resource planning
- **Get AI Insights**: Receive actionable recommendations powered by Snowflake Cortex AI

### Key Features

✅ **No Code Changes Required** - Connect any table by mapping your columns  
✅ **Professional UI** - Built with Streamlit for ease of use  
✅ **Advanced Analytics** - Powered by Snowpark Python and Snowflake ML  
✅ **AI-Powered** - Leverages Snowflake Cortex for intelligent insights  
✅ **Social Impact Focus** - Designed for Health and Education programs  

---

## 📁 Project Structure

```
ImpactGuard_AI/
├── manifest.yml                 # App manifest (version, privileges, setup script)
├── environment.yml              # Python dependencies
├── README.md                    # This file
├── scripts/
│   └── setup_script.sql        # Creates schemas, roles, procedures, Streamlit
└── streamlit/
    └── app.py                  # Main Streamlit application
```

---

## 🚀 Installation

### Prerequisites

- Snowflake account with Native App Framework enabled
- Privileges to create applications
- Access to Snowflake Cortex AI (for AI Insights feature)
- Access to a warehouse for compute

### Deployment Steps

1. **Upload the Application Package**
   ```sql
   -- Create application package
   CREATE APPLICATION PACKAGE impactguard_ai_package;
   
   -- Upload files to stage
   PUT file://manifest.yml @impactguard_ai_package.stage;
   PUT file://environment.yml @impactguard_ai_package.stage;
   PUT file://scripts/setup_script.sql @impactguard_ai_package.stage/scripts/;
   PUT file://streamlit/app.py @impactguard_ai_package.stage/streamlit/;
   ```

2. **Create Application Version**
   ```sql
   ALTER APPLICATION PACKAGE impactguard_ai_package
     ADD VERSION V1_0 USING '@impactguard_ai_package.stage';
   ```

3. **Install the Application**
   ```sql
   CREATE APPLICATION impactguard_ai
     FROM APPLICATION PACKAGE impactguard_ai_package
     USING VERSION V1_0;
   ```

4. **Grant Necessary Privileges**
   ```sql
   -- Grant warehouse usage
   GRANT USAGE ON WAREHOUSE <your_warehouse> TO APPLICATION impactguard_ai;
   
   -- Grant database access (for the databases you want to analyze)
   GRANT USAGE ON DATABASE <your_database> TO APPLICATION impactguard_ai;
   GRANT USAGE ON SCHEMA <your_database>.<your_schema> TO APPLICATION impactguard_ai;
   GRANT SELECT ON ALL TABLES IN SCHEMA <your_database>.<your_schema> TO APPLICATION impactguard_ai;
   ```

5. **Launch the Application**
   ```sql
   -- Open Streamlit UI
   SHOW STREAMLITS IN APPLICATION impactguard_ai;
   ```
   
   Click on the Streamlit URL to access the application.

---

## 📖 User Guide

### Step 1: Configure Your Data Source

1. Open the application in your browser
2. In the sidebar, select:
   - **Database**: Your source database
   - **Schema**: Your source schema
   - **Table**: The table you want to analyze

### Step 2: Map Your Columns

Identify which columns represent:
- **📅 Date Column**: Timestamp or date field
- **📊 Value/Metric Column**: Numeric field to analyze (e.g., patient visits, student enrollment)
- **🏷️ Category Column**: Optional grouping field (e.g., program type, region)

Click **"Save Configuration"** to proceed.

### Step 3: Explore the Tabs

#### 🔍 Data Quality Tab
- Click **"Run Quality Check"** to analyze your data
- View quality score (0-100)
- See detailed breakdowns of:
  - Null values by column
  - Duplicate records
  - Statistical outliers
- Get recommendations for improvement

#### 📈 Forecast Tab
- Click **"Generate Forecast"** to predict the next 4 weeks
- View model performance metrics (R² score)
- Explore interactive visualization
- Download forecast as CSV

#### 🤖 AI Insights Tab
- Click **"Generate AI Insights"** to get recommendations
- Receive 3 actionable bullet points
- View data distribution and statistics
- Understand trends and patterns

---

## 🛠️ Technical Architecture

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Snowflake Native App Framework |
| **UI** | Streamlit 1.28+ |
| **Data Processing** | Snowpark Python 1.11+ |
| **Machine Learning** | Snowflake ML Python 1.1+ |
| **AI** | Snowflake Cortex (Mistral-Large) |
| **Visualization** | Plotly 5.17+ |

### Data Flow

```
User Input (Streamlit UI)
    ↓
Configuration Saved (Session State)
    ↓
Stored Procedures Called (Snowpark)
    ↓
Data Processing & ML (Python UDFs)
    ↓
Results Returned (JSON)
    ↓
Visualization (Plotly Charts)
    ↓
AI Insights (Cortex API)
```

### Key Components

1. **manifest.yml**: Defines app metadata, version, and required privileges
2. **setup_script.sql**: Creates application objects (schemas, procedures, Streamlit)
3. **Stored Procedures**:
   - `check_data_quality()`: Analyzes nulls, duplicates, outliers
   - `generate_forecast()`: Creates 4-week predictions using linear regression
4. **Streamlit App**: User interface with configuration, analysis, and insights

---

## 🔒 Security & Permissions

### Required Privileges

The application requires the following privileges to function:

- `CREATE DATABASE` - For application database
- `CREATE SCHEMA` - For versioned schemas
- `CREATE TABLE` - For temporary data storage
- `CREATE VIEW` - For data transformations
- `CREATE STREAMLIT` - For UI hosting
- `CREATE PROCEDURE` - For Snowpark functions
- `USAGE ON WAREHOUSE` - For compute
- Access to `SNOWFLAKE.CORTEX.COMPLETE` - For AI insights

### Data Privacy

- The application only accesses tables you explicitly grant access to
- No data is stored permanently; all processing is ephemeral
- AI insights are generated using Snowflake Cortex (data stays in your account)

---

## 🎨 Customization

### Modifying the Forecast Model

To use a different ML model, edit `setup_script.sql`:

```python
# Replace LinearRegression with your preferred model
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)
```

### Changing the AI Model

To use a different Cortex model, edit `streamlit/app.py`:

```python
# Change 'mistral-large' to another model
cortex_query = f"""
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'llama2-70b-chat',  # or 'mixtral-8x7b', 'mistral-7b'
    '{prompt}'
) AS insights
"""
```

### Customizing the UI

The Streamlit app uses custom CSS. Modify the `st.markdown()` section in `app.py` to change colors, fonts, and styling.

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Cortex function not found"  
**Solution**: Ensure Snowflake Cortex is enabled in your account. Contact Snowflake support if needed.

**Issue**: "Insufficient privileges"  
**Solution**: Grant the application access to your warehouse and databases (see Installation step 4).

**Issue**: "Not enough data for forecasting"  
**Solution**: Ensure your table has at least 7 records with valid date and value columns.

**Issue**: "Column not found"  
**Solution**: Verify your column mappings match the actual column names in your table (case-sensitive).

---

## 📊 Use Cases

### Health Programs
- **Patient Visit Forecasting**: Predict clinic attendance for staffing
- **Supply Chain Monitoring**: Detect anomalies in medical supply data
- **Program Impact Analysis**: Analyze health outcome metrics

### Education Programs
- **Enrollment Forecasting**: Predict student enrollment for resource planning
- **Attendance Monitoring**: Identify patterns and outliers in attendance data
- **Performance Tracking**: Analyze test scores and learning outcomes

---

## 🤝 Contributing

This is a template application designed for customization. To extend functionality:

1. Add new stored procedures in `setup_script.sql`
2. Create new tabs in `streamlit/app.py`
3. Update `manifest.yml` with new version numbers
4. Test thoroughly before deployment

---

## 📄 License

This project is provided as-is for educational and social impact purposes.

---

## 🙏 Acknowledgments

Built with:
- **Snowflake Native App Framework**
- **Streamlit** for beautiful UIs
- **Snowpark Python** for distributed computing
- **Snowflake Cortex AI** for intelligent insights

**Dedicated to program managers making a difference in Health and Education** ❤️

---

## 📞 Support

For questions or issues:
1. Check the Troubleshooting section above
2. Review Snowflake Native App documentation
3. Consult your Snowflake account team

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Theme**: AI for Good 🌍
