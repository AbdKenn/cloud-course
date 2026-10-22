Here’s a step-by-step example to guide your students through using the fraud detection dataset (`bigquery-public-data.ml_datasets.ulb_fraud_detection`) by exporting it to Google Cloud Storage, loading it into a Dataproc cluster, performing some data transformation using PySpark, and training a logistic regression model using Spark MLlib.

### **Step 1: Export the Fraud Detection Dataset from BigQuery to Google Cloud Storage**

1. **BigQuery SQL Query to Get the Fraud Detection Data**  
   Run this query in BigQuery to select the dataset:

```sql
SELECT 
  V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
  V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
  V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class
FROM `bigquery-public-data.ml_datasets.ulb_fraud_detection`
```

2. **Export Data to Google Cloud Storage (GCS)**
   After running the query, click on "Export" in the BigQuery console and choose "Export to GCS".
   
   - Create a bucket in Google Cloud Storage (e.g., `gs://fraud-detection-bucket`) if you don’t have one.
   - Choose CSV format for export.
   - Example path: `gs://fraud-detection-bucket/fraud_detection.csv`

### **Step 2: Set Up a Dataproc Cluster**

To perform distributed data processing, we need to create a Dataproc cluster. Here's how:

1. **Create a Dataproc Cluster**:
   - Go to the Google Cloud Console.
   - Navigate to "Dataproc" → "Clusters" → "Create cluster."
   - Use the default configuration for most settings.
   - Make sure the cluster has Spark installed (which is available by default in most Dataproc setups).
   
2. **Upload Your Script**:  
   You can either upload your PySpark script (shown in the next steps) to the Dataproc cluster or run it interactively from a Jupyter Notebook hosted on the cluster.

### **Step 3: PySpark Code for Data Transformation and Logistic Regression**

Once the Dataproc cluster is set up, follow these steps to load the data from Cloud Storage, perform some data cleaning, and train a model using Spark MLlib.

1. **Load and Transform the Data**

Here’s a PySpark script that loads the fraud detection data from Google Cloud Storage, transforms it, and trains a logistic regression model.

```python
# Import required libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Create a Spark session
spark = SparkSession.builder \
    .appName("Fraud Detection with Logistic Regression") \
    .getOrCreate()

# Load the dataset from Google Cloud Storage
data_path = "gs://fraud-detection-bucket/fraud_detection.csv"
df = spark.read.csv(data_path, header=True, inferSchema=True)

# Inspect the data
df.printSchema()
df.show(5)

# Data Transformation:
# 1. Assemble all feature columns into a feature vector
# 2. Keep the 'Class' column as the label (0 = non-fraud, 1 = fraud)

# Create a VectorAssembler to combine feature columns into a single vector
feature_columns = [col for col in df.columns if col != 'Class']  # Exclude the label column
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")

# Transform the dataset to have the 'features' column
df_transformed = assembler.transform(df)

# Select only the features and label ('Class') columns for training
final_data = df_transformed.select("features", col("Class").alias("label"))

# Split the data into training and test sets
train_data, test_data = final_data.randomSplit([0.8, 0.2], seed=42)

# Train a logistic regression model
lr = LogisticRegression(featuresCol="features", labelCol="label")
lr_model = lr.fit(train_data)

# Evaluate the model on the test set
test_results = lr_model.evaluate(test_data)

# Show the accuracy
evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
roc_auc = evaluator.evaluate(test_results.predictions)

print(f"ROC-AUC: {roc_auc:.4f}")

# Stop the Spark session
spark.stop()
```

### **Explanation of the Code**:

1. **SparkSession Creation**:  
   We initialize a `SparkSession` to interact with Spark. This is the entry point for any PySpark job.

2. **Loading Data from Cloud Storage**:  
   The `spark.read.csv` function loads the fraud detection CSV file from Google Cloud Storage into a Spark DataFrame.

3. **Data Transformation**:  
   - The `VectorAssembler` is used to combine all the feature columns (`V1, V2, ..., V28, Amount`) into a single column named `features`. This is required by Spark MLlib to run the logistic regression.
   - We rename the `Class` column to `label` since that is what Spark expects for the classification target.

4. **Train/Test Split**:  
   The data is split into an 80/20 ratio for training and testing.

5. **Logistic Regression Model**:  
   A simple logistic regression model is trained using the `features` column as input and the `label` column as the output. The logistic regression model is part of the `pyspark.ml.classification` package.

6. **Model Evaluation**:  
   The `BinaryClassificationEvaluator` evaluates the model using the ROC-AUC metric, which measures the ability of the model to distinguish between fraud and non-fraud cases.

### **Step 4: Running the Script on the Dataproc Cluster**

You can either:
- Copy the script to the master node of your Dataproc cluster and run it using `spark-submit`.
- Or, run it interactively from a notebook environment in the Dataproc cluster.

Here’s how to run the script using `spark-submit` from the master node:

```bash
gcloud dataproc jobs submit pyspark gs://fraud-detection-bucket/fraud_detection.py \
    --cluster=your-dataproc-cluster-name \
    --region=your-region
```

### **Step 5: Monitoring and Evaluating the Model**

- After the model runs, you will see the evaluation output (`ROC-AUC score`) in the logs.
- You can tune this by trying different algorithms, hyperparameters, or transformations.

### **Summary**:
- **Step 1**: Export the dataset from BigQuery to Google Cloud Storage.
- **Step 2**: Set up a Dataproc cluster.
- **Step 3**: Load the data into PySpark, transform it, and train a logistic regression model.
- **Step 4**: Submit the PySpark job to the Dataproc cluster and evaluate the model performance.

This workflow demonstrates end-to-end data handling, from storage to processing and machine learning on GCP using Dataproc and PySpark. Let me know if you need further clarifications!