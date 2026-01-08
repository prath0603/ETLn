from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, split, trim,
    current_timestamp, to_timestamp
)
import os

# =========================
# Spark Session
# =========================
spark = SparkSession.builder \
    .appName("KafkaSparkETL_S3") \
    .config(
        "spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
    ) \
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# =========================
# Kafka Source
# =========================
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "log-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Kafka value → string
raw_df = df.selectExpr("CAST(value AS STRING) AS raw_json")

# Extract log_line from JSON string
logs_df = raw_df.select(
    split(col("raw_json"), "\"")[3].alias("log_line")
)

# =========================
# Parse log line
# =========================
parts = split(col("log_line"), " \\| ")

parsed_df = logs_df.select(
    split(parts[0], "=")[1].cast("int").alias("sno"),

    to_timestamp(
        trim(parts[1]),
        "yyyy-MM-dd HH:mm:ss.SSSSSS"
    ).alias("timestamp"),

    trim(parts[2]).alias("level"),

    split(parts[3], "=")[1].cast("int").alias("request_id"),
    split(parts[4], "=")[1].cast("int").alias("user_id"),
    split(parts[5], "=")[1].cast("int").alias("response_time"),
    split(parts[6], "=")[1].cast("int").alias("status"),

    current_timestamp().alias("processed_at")
)

# Drop bad rows
final_df = parsed_df.na.drop(
    subset=["request_id", "user_id", "timestamp"]
)

# =========================
# Debug (optional)
# =========================
final_df.printSchema()

# =========================
# Console Sink for Debug
# =========================
final_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

# =========================
# Write to S3 (FINAL SINK)
# =========================
query = final_df.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option(
        "path",
        "s3a://thoughtwin-etl-bucket-2025/processed/logs/"
    ) \
    .option(
        "checkpointLocation",
        "s3a://thoughtwin-etl-bucket-2025/checkpoints/logs_etl/"
    ) \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()
