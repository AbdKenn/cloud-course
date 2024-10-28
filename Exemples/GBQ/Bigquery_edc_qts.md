Here are a few examples that use public datasets on BigQuery. I'll include simple SQL questions for querying data, as well as a machine learning example using BigQuery ML.

### 1. **Basic SQL Queries using Public Datasets**

**Dataset**: `bigquery-public-data.usa_names.usa_1910_2013`

**Question**: What were the top 5 most popular baby names in the USA in 2010?
```sql

```

**Question**: How many babies were born with the name "John" between 2000 and 2010?
```sql

```

### 2. **Intermediate SQL Queries using Public Datasets**

**Dataset**: `bigquery-public-data.covid19_jhu_csse.summary`

**Question**: What are the top 10 countries with the highest number of COVID-19 cases in 2021?
```sql

```

**Question**: Calculate the global average daily COVID-19 cases for 2021.
```sql

```

### 3. **BigQuery ML Example**

**Dataset**: `bigquery-public-data.ml_datasets.ulb_fraud_detection`

**Question**: Create a machine learning model to predict fraudulent transactions.

First, we create a logistic regression model to classify fraudulent transactions.

```sql

```

To evaluate the model's performance:
```sql

```

To use the model for predictions:
```sql

```



Here are some additional questions and their corresponding SQL queries using the COVID-19 public dataset in BigQuery (`bigquery-public-data.covid19_jhu_csse.summary`).

### 1. **Total COVID-19 Cases and Deaths in 2021 by Continent**

**Question**: What are the total COVID-19 cases and deaths in each continent for the year 2021?

```sql

```

### 2. **Daily New Cases and Deaths in the USA in 2021**

**Question**: How many new COVID-19 cases and deaths were recorded each day in the USA in 2021?

```sql

```

### 3. **Top 10 Countries with the Highest Case Fatality Rate in 2021**

**Question**: Which 10 countries had the highest case fatality rate (deaths/cases) in 2021?

```sql

```

### 4. **Countries with the Highest Recovery Rate in 2021**

**Question**: What are the top 10 countries with the highest COVID-19 recovery rate in 2021?

```sql

```

### 5. **Monthly COVID-19 Case Growth in India in 2021**

**Question**: How did COVID-19 cases grow month by month in India in 2021?

```sql

```

### 6. **Countries with No Deaths Recorded in 2021**

**Question**: Which countries did not report any COVID-19 deaths in 2021?

```sql

```

### 7. **Daily Cases and Deaths in Brazil Between June and August 2021**

**Question**: What were the daily COVID-19 cases and deaths in Brazil from June to August 2021?

```sql

```

### 8. **Countries with a Decline in Cases at the End of 2021**

**Question**: Which countries saw a decline in COVID-19 cases in December 2021 compared to November 2021?

```sql

```

These examples provide a good mix of query complexity and showcase various data aggregation techniques on BigQuery for students to practice and understand SQL fundamentals while exploring COVID-19 data trends. Let me know if you’d like further breakdowns or advanced examples!