# ImpactGuard AI - Deployment Guide

## Quick Start Deployment

### Option 1: Using SnowSQL (Recommended)

```bash
# 1. Navigate to project directory
cd ImpactGuard_AI

# 2. Connect to Snowflake
snowsql -a <account> -u <username>

# 3. Create application package
CREATE APPLICATION PACKAGE IF NOT EXISTS impactguard_ai_package;

# 4. Create stage
CREATE STAGE IF NOT EXISTS impactguard_ai_package.app_stage;

# 5. Upload files
PUT file://manifest.yml @impactguard_ai_package.app_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://environment.yml @impactguard_ai_package.app_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://scripts/setup_script.sql @impactguard_ai_package.app_stage/scripts/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://streamlit/app.py @impactguard_ai_package.app_stage/streamlit/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

# 6. Create version
ALTER APPLICATION PACKAGE impactguard_ai_package
  ADD VERSION V1_0 USING '@impactguard_ai_package.app_stage';

# 7. Create application
CREATE APPLICATION IF NOT EXISTS impactguard_ai
  FROM APPLICATION PACKAGE impactguard_ai_package
  USING VERSION V1_0;

# 8. Grant warehouse access
GRANT USAGE ON WAREHOUSE <your_warehouse> TO APPLICATION impactguard_ai;

# 9. Launch Streamlit
SHOW STREAMLITS IN APPLICATION impactguard_ai;
```

### Option 2: Using Snowsight UI

1. **Upload Files**
   - Go to Snowsight → Data → Databases
   - Create a new database for the application package
   - Upload files via the UI

2. **Create Application**
   - Go to Apps → Create App
   - Select "From Package"
   - Follow the wizard

3. **Configure Permissions**
   - Grant warehouse usage
   - Grant database/schema access

---

## Post-Deployment Configuration

### Grant Data Access

```sql
-- Grant access to your data database
GRANT USAGE ON DATABASE <your_data_db> TO APPLICATION impactguard_ai;
GRANT USAGE ON ALL SCHEMAS IN DATABASE <your_data_db> TO APPLICATION impactguard_ai;
GRANT SELECT ON ALL TABLES IN SCHEMA <your_data_db>.<schema> TO APPLICATION impactguard_ai;
GRANT SELECT ON FUTURE TABLES IN SCHEMA <your_data_db>.<schema> TO APPLICATION impactguard_ai;
```

### Enable Cortex AI (if not already enabled)

```sql
-- Check Cortex availability
SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', 'Hello') AS test;

-- If error, contact Snowflake support to enable Cortex in your account
```

---

## Testing the Application

### Test Data Quality Check

```sql
-- Call the procedure directly
CALL impactguard_ai.app_schema.check_data_quality(
    '<database>',
    '<schema>',
    '<table>',
    '<value_column>',
    '<date_column>',
    '<category_column>'
);
```

### Test Forecast Generation

```sql
-- Call the forecast procedure
CALL impactguard_ai.app_schema.generate_forecast(
    '<database>',
    '<schema>',
    '<table>',
    '<value_column>',
    '<date_column>',
    '<category_column>'
);
```

---

## Updating the Application

### Deploy New Version

```bash
# 1. Upload updated files
PUT file://streamlit/app.py @impactguard_ai_package.app_stage/streamlit/ OVERWRITE=TRUE;

# 2. Create new version
ALTER APPLICATION PACKAGE impactguard_ai_package
  ADD VERSION V1_1 USING '@impactguard_ai_package.app_stage';

# 3. Upgrade application
ALTER APPLICATION impactguard_ai UPGRADE USING VERSION V1_1;
```

---

## Monitoring & Maintenance

### Check Application Status

```sql
-- View application details
SHOW APPLICATIONS LIKE 'impactguard_ai';

-- View Streamlit status
SHOW STREAMLITS IN APPLICATION impactguard_ai;

-- View procedures
SHOW PROCEDURES IN SCHEMA impactguard_ai.app_schema;
```

### View Logs

```sql
-- Check query history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE QUERY_TEXT ILIKE '%impactguard%'
ORDER BY START_TIME DESC
LIMIT 100;
```

---

## Uninstallation

```sql
-- Drop application
DROP APPLICATION IF EXISTS impactguard_ai;

-- Drop application package (optional)
DROP APPLICATION PACKAGE IF EXISTS impactguard_ai_package;
```

---

## Production Checklist

- [ ] Application package created
- [ ] All files uploaded to stage
- [ ] Version created successfully
- [ ] Application installed
- [ ] Warehouse access granted
- [ ] Database access granted
- [ ] Cortex AI enabled and tested
- [ ] Streamlit UI accessible
- [ ] Data quality check tested
- [ ] Forecast generation tested
- [ ] AI insights tested
- [ ] User training completed
- [ ] Documentation shared with users

---

## Troubleshooting Deployment

**Issue**: "File not found in stage"  
**Solution**: Verify file paths and use `LIST @stage` to check uploaded files

**Issue**: "Version already exists"  
**Solution**: Use a different version name (e.g., V1_1, V1_2)

**Issue**: "Application role not found"  
**Solution**: Ensure setup_script.sql ran successfully

**Issue**: "Streamlit not showing"  
**Solution**: Check `SHOW STREAMLITS` and verify warehouse is running

---

**For additional support, consult Snowflake Native App Framework documentation.**
