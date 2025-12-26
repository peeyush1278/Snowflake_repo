# ImpactGuard AI - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Deploy to Snowflake (2 minutes)

```sql
-- 1. Create application package
CREATE APPLICATION PACKAGE impactguard_ai_package;
CREATE STAGE impactguard_ai_package.app_stage;

-- 2. Upload files (use SnowSQL or Snowsight UI)
PUT file://manifest.yml @impactguard_ai_package.app_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://environment.yml @impactguard_ai_package.app_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://scripts/setup_script.sql @impactguard_ai_package.app_stage/scripts/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://streamlit/app.py @impactguard_ai_package.app_stage/streamlit/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- 3. Create version and install
ALTER APPLICATION PACKAGE impactguard_ai_package
  ADD VERSION V1_0 USING '@impactguard_ai_package.app_stage';

CREATE APPLICATION impactguard_ai
  FROM APPLICATION PACKAGE impactguard_ai_package
  USING VERSION V1_0;

-- 4. Grant permissions
GRANT USAGE ON WAREHOUSE <your_warehouse> TO APPLICATION impactguard_ai;
GRANT USAGE ON DATABASE <your_database> TO APPLICATION impactguard_ai;
GRANT USAGE ON SCHEMA <your_database>.<your_schema> TO APPLICATION impactguard_ai;
GRANT SELECT ON ALL TABLES IN SCHEMA <your_database>.<your_schema> TO APPLICATION impactguard_ai;
```

### Step 2: Create Test Data (1 minute)

```sql
-- Run the sample data script from SAMPLE_DATA.md
-- This creates 3 test tables: patient_visits, student_enrollment, supply_distribution
```

### Step 3: Launch the App (30 seconds)

```sql
-- Get Streamlit URL
SHOW STREAMLITS IN APPLICATION impactguard_ai;
```

Click the URL to open the application.

### Step 4: Configure & Analyze (1 minute)

1. **Select Data Source**:
   - Database: `IMPACTGUARD_TEST`
   - Schema: `HEALTH_PROGRAMS`
   - Table: `PATIENT_VISITS`

2. **Map Columns**:
   - Date: `VISIT_DATE`
   - Value: `PATIENT_COUNT`
   - Category: `PROGRAM_TYPE`

3. **Click "Save Configuration"**

4. **Try Each Tab**:
   - 🔍 Data Quality → Click "Run Quality Check"
   - 📈 Forecast → Click "Generate Forecast"
   - 🤖 AI Insights → Click "Generate AI Insights"

---

## 📋 Common Use Cases

### Health Programs

**Patient Visit Forecasting**
- Table: Patient visit records
- Date: Visit date
- Value: Number of patients
- Category: Program type or clinic location

**Supply Chain Monitoring**
- Table: Supply distribution records
- Date: Distribution date
- Value: Quantity distributed
- Category: Supply type

### Education Programs

**Student Enrollment Prediction**
- Table: Enrollment records
- Date: Enrollment date
- Value: Number of students
- Category: Grade level or school

**Attendance Tracking**
- Table: Daily attendance records
- Date: Attendance date
- Value: Attendance count
- Category: Class or program

---

## 🎯 Expected Results

### Data Quality Tab
- **Quality Score**: 0-100 rating
- **Null Analysis**: Count and percentage by column
- **Duplicates**: Number of duplicate records
- **Outliers**: Statistical outliers with sample indices
- **Recommendations**: Actionable next steps

### Forecast Tab
- **Model Metrics**: R² score, coefficients
- **Visualization**: Interactive chart with historical + forecast
- **Forecast Table**: 28 days of predictions
- **Download**: CSV export option

### AI Insights Tab
- **Action Plan**: 3 AI-generated recommendations
- **Data Summary**: Key statistics
- **Distribution**: Histogram of values

---

## 🔧 Troubleshooting

**Problem**: "Cortex function not found"  
**Solution**: Contact Snowflake support to enable Cortex AI

**Problem**: "Insufficient privileges"  
**Solution**: Run the GRANT statements from Step 1

**Problem**: "Not enough data for forecasting"  
**Solution**: Ensure at least 7 records with valid dates and values

**Problem**: "Column not found"  
**Solution**: Check column names are exact (case-sensitive)

---

## 📞 Next Steps

1. ✅ Test with sample data
2. ✅ Connect your real data
3. ✅ Share with your team
4. ✅ Schedule regular quality checks
5. ✅ Use forecasts for planning

---

**Need More Help?**
- Full documentation: [README.md](README.md)
- Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Sample data: [SAMPLE_DATA.md](SAMPLE_DATA.md)

---

**Built with ❤️ for Social Impact Programs**
