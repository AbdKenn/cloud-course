Here are a few examples that use public datasets on BigQuery. I'll include simple SQL questions for querying data, as well as a machine learning example using BigQuery ML.

### 1. **Basic SQL Queries using Public Datasets**

**Dataset**: `bigquery-public-data.usa_names.usa_1910_2013`

**Question**: What were the top 5 most popular baby names in the USA in 2010?
```sql
SELECT name, SUM(number) as total
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE year = 2010
GROUP BY name
ORDER BY total DESC
LIMIT 5;
```

**Question**: How many babies were born with the name "John" between 2000 and 2010?
```sql
SELECT SUM(number) as total_born
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE name = 'John' AND year BETWEEN 2000 AND 2010;
```

### 2. **Intermediate SQL Queries using Public Datasets**

**Dataset**: `bigquery-public-data.covid19_jhu_csse.summary`

**Question**: What are the top 10 countries with the highest number of COVID-19 cases in 2021?
```sql
SELECT country_region, SUM(confirmed) as total_cases
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021
GROUP BY country_region
ORDER BY total_cases DESC
LIMIT 10;
```

**Question**: Calculate the global average daily COVID-19 cases for 2021.
```sql
SELECT AVG(confirmed) as avg_daily_cases
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021;
```

### 3. **BigQuery ML Example**

**Dataset**: `bigquery-public-data.ml_datasets.ulb_fraud_detection`

**Question**: Create a machine learning model to predict fraudulent transactions.

First, we create a logistic regression model to classify fraudulent transactions.

```sql
CREATE OR REPLACE MODEL `my_project.my_dataset.fraud_detection_model`
OPTIONS(model_type='logistic_reg', input_label_cols=['Class']) AS
SELECT
    V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
    V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
    V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class
FROM `bigquery-public-data.ml_datasets.ulb_fraud_detection`
WHERE Class IS NOT NULL;
```

To evaluate the model's performance:
```sql
SELECT *
FROM ML.EVALUATE(MODEL `my_project.my_dataset.fraud_detection_model`);
```

To use the model for predictions:
```sql
SELECT *
FROM ML.PREDICT(MODEL `my_project.my_dataset.fraud_detection_model`,
  (SELECT * FROM `bigquery-public-data.ml_datasets.ulb_fraud_detection`
   LIMIT 100));
```



Here are some additional questions and their corresponding SQL queries using the COVID-19 public dataset in BigQuery (`bigquery-public-data.covid19_jhu_csse.summary`).

### 1. **Total COVID-19 Cases and Deaths in 2021 by Continent**

**Question**: What are the total COVID-19 cases and deaths in each continent for the year 2021?

```sql
SELECT continent_region, 
       SUM(confirmed) AS total_cases, 
       SUM(deaths) AS total_deaths
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021
GROUP BY continent_region
ORDER BY total_cases DESC;
```

### 2. **Daily New Cases and Deaths in the USA in 2021**

**Question**: How many new COVID-19 cases and deaths were recorded each day in the USA in 2021?

```sql
SELECT date, 
       confirmed AS daily_cases, 
       deaths AS daily_deaths
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE country_region = 'US' AND EXTRACT(YEAR FROM date) = 2021
ORDER BY date;
```

### 3. **Top 10 Countries with the Highest Case Fatality Rate in 2021**

**Question**: Which 10 countries had the highest case fatality rate (deaths/cases) in 2021?

```sql
SELECT country_region,
       SUM(deaths) AS total_deaths,
       SUM(confirmed) AS total_cases,
       SAFE_DIVIDE(SUM(deaths), SUM(confirmed)) AS case_fatality_rate
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021
GROUP BY country_region
HAVING total_cases > 10000  -- Filter for countries with at least 10,000 cases
ORDER BY case_fatality_rate DESC
LIMIT 10;
```

### 4. **Countries with the Highest Recovery Rate in 2021**

**Question**: What are the top 10 countries with the highest COVID-19 recovery rate in 2021?

```sql
SELECT country_region, 
       SUM(recovered) AS total_recovered, 
       SUM(confirmed) AS total_cases,
       SAFE_DIVIDE(SUM(recovered), SUM(confirmed)) AS recovery_rate
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021
GROUP BY country_region
HAVING total_cases > 10000  -- Filter for countries with at least 10,000 cases
ORDER BY recovery_rate DESC
LIMIT 10;
```

### 5. **Monthly COVID-19 Case Growth in India in 2021**

**Question**: How did COVID-19 cases grow month by month in India in 2021?

```sql
SELECT EXTRACT(MONTH FROM date) AS month, 
       SUM(confirmed) AS total_cases
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE country_region = 'India' AND EXTRACT(YEAR FROM date) = 2021
GROUP BY month
ORDER BY month;
```

### 6. **Countries with No Deaths Recorded in 2021**

**Question**: Which countries did not report any COVID-19 deaths in 2021?

```sql
SELECT DISTINCT country_region
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021
GROUP BY country_region
HAVING SUM(deaths) = 0;
```

### 7. **Daily Cases and Deaths in Brazil Between June and August 2021**

**Question**: What were the daily COVID-19 cases and deaths in Brazil from June to August 2021?

```sql
SELECT date, 
       confirmed AS daily_cases, 
       deaths AS daily_deaths
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE country_region = 'Brazil' 
  AND date BETWEEN '2021-06-01' AND '2021-08-31'
ORDER BY date;
```

### 8. **Countries with a Decline in Cases at the End of 2021**

**Question**: Which countries saw a decline in COVID-19 cases in December 2021 compared to November 2021?

```sql
SELECT country_region,
       SUM(CASE WHEN EXTRACT(MONTH FROM date) = 12 THEN confirmed ELSE 0 END) AS december_cases,
       SUM(CASE WHEN EXTRACT(MONTH FROM date) = 11 THEN confirmed ELSE 0 END) AS november_cases
FROM `bigquery-public-data.covid19_jhu_csse.summary`
WHERE EXTRACT(YEAR FROM date) = 2021
GROUP BY country_region
HAVING december_cases < november_cases
ORDER BY november_cases - december_cases DESC;
```

These examples provide a good mix of query complexity and showcase various data aggregation techniques on BigQuery for students to practice and understand SQL fundamentals while exploring COVID-19 data trends. Let me know if you’d like further breakdowns or advanced examples!