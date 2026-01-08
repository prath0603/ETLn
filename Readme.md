# 🚀 Real-Time Log-Based ETL Pipeline (Kafka + PySpark + Amazon S3)

This project implements a **production-grade, end-to-end real-time ETL (Extract, Transform, Load) pipeline** that simulates continuous application log generation, streams data using **Apache Kafka (KRaft mode)**, processes it using **PySpark Structured Streaming**, and persists the transformed data into **Amazon S3** in **Parquet format**.

The pipeline is designed to closely resemble **real-world log ingestion and data lake architectures** used in modern data engineering platforms for observability, analytics, and downstream processing.

---

## Architecture & Data Flow

Python Log Generator
↓
Append-only Log File (app.log)
↓
Kafka File Producer
↓
Kafka Topic
↓
PySpark Structured Streaming
↓
Amazon S3 (Parquet Format)

---

## Pipeline Explanation

The pipeline starts with a Python-based log generator that continuously produces synthetic application logs and appends them to an `app.log` file. Each log entry contains a serial number, timestamp, log level, and message, simulating real application behavior.

A custom Kafka file producer monitors this append-only log file and uses an offset-tracking mechanism to ensure that **only newly added log entries** are published to a Kafka topic. This approach prevents duplicate processing and ensures fault tolerance across restarts.

PySpark Structured Streaming then consumes the log data from Kafka in real time. The raw log messages are parsed into a structured schema, appropriate data types are enforced, and additional metadata such as ingestion timestamp is added. The streaming job processes data continuously in micro-batches.

Finally, the transformed and enriched data is written directly to **Amazon S3** in **Parquet format**, enabling efficient storage, faster analytical queries, and seamless integration with downstream analytics tools.

---

## Technology Stack

- Python 3  
- Apache Kafka (KRaft mode – no Zookeeper)  
- Apache Spark (PySpark Structured Streaming)  
- Amazon S3  
- Parquet  
- Linux / Unix  

---

## Prerequisites

- Python 3.8 or higher  
- Apache Kafka 3.x configured in KRaft mode  
- Apache Spark 3.x with PySpark  
- AWS account with S3 access  
- AWS CLI configured with valid credentials  
- Required Python libraries listed in `requirements.txt`  

---

## Setup & Execution

Activate the virtual environment:

```bash
source venv/bin/activate

Start Kafka (KRaft mode):

kafka-server-start.sh config/server.properties

Create the Kafka topic:

kafka-topics.sh --create \
  --topic logs-topic \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1


Start the log generator:

python log_generator/generate_logs.py

Start the Kafka file producer:

python kafka_producer/file_producer.py


Run the PySpark streaming ETL job:

spark-submit spark_consumer/spark_etl.py

Output

The processed logs are continuously written to Amazon S3 in Parquet format.
The data is optimized for analytics and ready for downstream consumption.

Key Concepts Demonstrated

Real-time ETL pipeline design

Log-based data ingestion

Kafka producer–consumer architecture

File offset management

PySpark Structured Streaming

Cloud-based data lake ingestion using Amazon S3

Columnar storage with Parquet

Learning Outcome

This project demonstrates how real-time streaming pipelines are built in production environments, combining file-based log ingestion, distributed messaging systems, stream processing frameworks, and cloud-based data lake storage into a scalable and fault-tolerant architecture.

Author

Prathmesh Saxena
Aspiring Data Engineer | Real-Time Data Pipelines | Big Data & Cloud


.

