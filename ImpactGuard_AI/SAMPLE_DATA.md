# ImpactGuard AI - Sample Data Generator

This script creates sample data for testing the ImpactGuard AI application.

## Usage

Run this SQL in your Snowflake account to create test data:

```sql
-- Create a test database and schema
CREATE DATABASE IF NOT EXISTS impactguard_test;
CREATE SCHEMA IF NOT EXISTS impactguard_test.health_programs;

USE SCHEMA impactguard_test.health_programs;

-- ============================================================================
-- Sample 1: Patient Visits Data (Health Program)
-- ============================================================================

CREATE OR REPLACE TABLE patient_visits (
    visit_date DATE,
    patient_count NUMBER,
    program_type VARCHAR(50),
    region VARCHAR(50)
);

-- Insert sample data with realistic patterns
INSERT INTO patient_visits
WITH date_series AS (
    SELECT DATEADD(day, SEQ4(), '2024-01-01') AS visit_date
    FROM TABLE(GENERATOR(ROWCOUNT => 180))  -- 6 months of data
)
SELECT 
    visit_date,
    -- Base patient count with weekly pattern and random variation
    ROUND(50 + 
          10 * SIN(DATEDIFF(day, '2024-01-01', visit_date) * 2 * PI() / 7) + 
          UNIFORM(0, 20, RANDOM())) AS patient_count,
    -- Program types
    CASE 
        WHEN MOD(DATEDIFF(day, '2024-01-01', visit_date), 3) = 0 THEN 'Vaccination'
        WHEN MOD(DATEDIFF(day, '2024-01-01', visit_date), 3) = 1 THEN 'Prenatal Care'
        ELSE 'General Checkup'
    END AS program_type,
    -- Regions
    CASE 
        WHEN MOD(DATEDIFF(day, '2024-01-01', visit_date), 4) = 0 THEN 'North'
        WHEN MOD(DATEDIFF(day, '2024-01-01', visit_date), 4) = 1 THEN 'South'
        WHEN MOD(DATEDIFF(day, '2024-01-01', visit_date), 4) = 2 THEN 'East'
        ELSE 'West'
    END AS region
FROM date_series;

-- Add some nulls for data quality testing
UPDATE patient_visits 
SET patient_count = NULL 
WHERE MOD(DATEDIFF(day, '2024-01-01', visit_date), 30) = 0;

-- Add some duplicates for data quality testing
INSERT INTO patient_visits 
SELECT * FROM patient_visits 
WHERE visit_date BETWEEN '2024-03-01' AND '2024-03-05';

-- Add some outliers
UPDATE patient_visits 
SET patient_count = 500 
WHERE visit_date = '2024-04-15';

SELECT 'Sample data created: patient_visits' AS status;

-- ============================================================================
-- Sample 2: Student Enrollment Data (Education Program)
-- ============================================================================

CREATE OR REPLACE TABLE student_enrollment (
    enrollment_date DATE,
    student_count NUMBER,
    grade_level VARCHAR(20),
    school_district VARCHAR(50)
);

-- Insert sample data
INSERT INTO student_enrollment
WITH date_series AS (
    SELECT DATEADD(week, SEQ4(), '2024-01-01') AS enrollment_date
    FROM TABLE(GENERATOR(ROWCOUNT => 26))  -- 26 weeks
)
SELECT 
    enrollment_date,
    -- Enrollment with growth trend
    ROUND(200 + 
          DATEDIFF(week, '2024-01-01', enrollment_date) * 2 + 
          UNIFORM(-10, 10, RANDOM())) AS student_count,
    -- Grade levels
    CASE 
        WHEN MOD(DATEDIFF(week, '2024-01-01', enrollment_date), 3) = 0 THEN 'Elementary'
        WHEN MOD(DATEDIFF(week, '2024-01-01', enrollment_date), 3) = 1 THEN 'Middle School'
        ELSE 'High School'
    END AS grade_level,
    -- School districts
    CASE 
        WHEN MOD(DATEDIFF(week, '2024-01-01', enrollment_date), 2) = 0 THEN 'District A'
        ELSE 'District B'
    END AS school_district
FROM date_series;

-- Add data quality issues
UPDATE student_enrollment 
SET student_count = NULL 
WHERE enrollment_date = '2024-02-05';

SELECT 'Sample data created: student_enrollment' AS status;

-- ============================================================================
-- Sample 3: Supply Distribution Data (Health Program)
-- ============================================================================

CREATE OR REPLACE TABLE supply_distribution (
    distribution_date DATE,
    quantity_distributed NUMBER,
    supply_type VARCHAR(50),
    facility_name VARCHAR(100)
);

-- Insert sample data
INSERT INTO supply_distribution
WITH date_series AS (
    SELECT DATEADD(day, SEQ4(), '2024-01-01') AS distribution_date
    FROM TABLE(GENERATOR(ROWCOUNT => 90))  -- 3 months
)
SELECT 
    distribution_date,
    -- Supply quantity with variation
    ROUND(100 + UNIFORM(0, 50, RANDOM())) AS quantity_distributed,
    -- Supply types
    CASE 
        WHEN MOD(DATEDIFF(day, '2024-01-01', distribution_date), 4) = 0 THEN 'Vaccines'
        WHEN MOD(DATEDIFF(day, '2024-01-01', distribution_date), 4) = 1 THEN 'Medical Supplies'
        WHEN MOD(DATEDIFF(day, '2024-01-01', distribution_date), 4) = 2 THEN 'Medications'
        ELSE 'PPE'
    END AS supply_type,
    -- Facilities
    CASE 
        WHEN MOD(DATEDIFF(day, '2024-01-01', distribution_date), 3) = 0 THEN 'Central Hospital'
        WHEN MOD(DATEDIFF(day, '2024-01-01', distribution_date), 3) = 1 THEN 'Community Clinic'
        ELSE 'Rural Health Center'
    END AS facility_name
FROM date_series;

SELECT 'Sample data created: supply_distribution' AS status;

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Check patient visits
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT visit_date) AS unique_dates,
    AVG(patient_count) AS avg_patients,
    SUM(CASE WHEN patient_count IS NULL THEN 1 ELSE 0 END) AS null_count
FROM patient_visits;

-- Check student enrollment
SELECT 
    COUNT(*) AS total_rows,
    MIN(enrollment_date) AS start_date,
    MAX(enrollment_date) AS end_date,
    AVG(student_count) AS avg_enrollment
FROM student_enrollment;

-- Check supply distribution
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT supply_type) AS supply_types,
    SUM(quantity_distributed) AS total_distributed
FROM supply_distribution;

SELECT '✅ All sample data created successfully!' AS final_status;
```

## Testing with ImpactGuard AI

### Test Configuration 1: Patient Visits

- **Database**: `IMPACTGUARD_TEST`
- **Schema**: `HEALTH_PROGRAMS`
- **Table**: `PATIENT_VISITS`
- **Date Column**: `VISIT_DATE`
- **Value Column**: `PATIENT_COUNT`
- **Category Column**: `PROGRAM_TYPE` or `REGION`

### Test Configuration 2: Student Enrollment

- **Database**: `IMPACTGUARD_TEST`
- **Schema**: `HEALTH_PROGRAMS`
- **Table**: `STUDENT_ENROLLMENT`
- **Date Column**: `ENROLLMENT_DATE`
- **Value Column**: `STUDENT_COUNT`
- **Category Column**: `GRADE_LEVEL`

### Test Configuration 3: Supply Distribution

- **Database**: `IMPACTGUARD_TEST`
- **Schema**: `HEALTH_PROGRAMS`
- **Table**: `SUPPLY_DISTRIBUTION`
- **Date Column**: `DISTRIBUTION_DATE`
- **Value Column**: `QUANTITY_DISTRIBUTED`
- **Category Column**: `SUPPLY_TYPE`

## Expected Results

### Data Quality Checks
- **Nulls**: Should detect intentionally added null values
- **Duplicates**: Should find duplicate records in patient_visits
- **Outliers**: Should identify the outlier value (500) in patient_visits
- **Quality Score**: Should be in the 70-85 range due to intentional issues

### Forecast
- **Patient Visits**: Should show weekly cyclical pattern
- **Student Enrollment**: Should show upward trend
- **Supply Distribution**: Should show relatively stable pattern

### AI Insights
- Should recommend addressing null values
- Should suggest investigating outliers
- Should provide resource allocation recommendations based on trends
