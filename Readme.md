📌 Project OverviewThis project implements a production-grade, end-to-end real-time ETL (Extract, Transform, Load) pipeline. It simulates continuous application log generation, streams data via Apache Kafka (KRaft mode), processes the stream with PySpark Structured Streaming, and persists the structured data into Amazon S3 in the highly optimized Parquet format.This architecture mimics modern observability and data lake ingestion patterns used by high-scale data platforms.🏗️ ArchitectureCode snippetgraph LR
    A[Python Log Generator] -->|Append| B(app.log)
    B --> C[Kafka File Producer]
    C --> D{{Kafka Topic}}
    D --> E[PySpark Structured Streaming]
    E -->|Write| F[Amazon S3 - Parquet]
🔄 ETL Pipeline Breakdown🔹 ExtractLog Generation: A Python script generates synthetic application logs (Timestamp, Log Level, Message).Intelligent Production: A custom Kafka Producer monitors the app.log file using an offset mechanism, ensuring only new entries are sent to the topic (avoiding duplicates or data loss upon restart).🔹 TransformSchema Enforcement: PySpark parses the raw Kafka strings into a structured DataFrame schema.Feature Engineering: Addition of ingestion metadata and timestamps to facilitate downstream partitioning and troubleshooting.🔹 LoadData Lake Ingestion: Transformed data is streamed directly to Amazon S3.Storage Optimization: Files are saved in Parquet format, which provides columnar storage for faster analytical queries and significant cost savings on storage.🧰 Tech StackLanguage: Python 3.xStreaming Platform: Apache Kafka (KRaft Mode)Processing Engine: PySpark (Structured Streaming)Cloud Storage: Amazon S3Data Format: Apache ParquetEnvironment: Linux/Unix⚙️ PrerequisitesPython 3.8+Apache Kafka 3.x+ (Configured for KRaft)Apache Spark 3.x (with Hadoop-AWS dependencies)AWS CLI configured with appropriate s3:PutObject permissions▶️ Setup & Execution1️⃣ Environment SetupBash# Clone the repository
git clone https://github.com/your-username/kafka-pyspark-etl.git
cd kafka-pyspark-etl

# Initialize virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2️⃣ Start Kafka (KRaft Mode)Since this project uses KRaft, we skip Zookeeper and use a cluster ID for metadata.Bash# Generate a Cluster ID
export KAFKA_CLUSTER_ID=$(sh bin/kafka-storage.sh random-uuid)

# Format Storage Directories
sh bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

# Start Kafka Server
sh bin/kafka-server-start.sh config/kraft/server.properties
3️⃣ Create Kafka TopicBashsh bin/kafka-topics.sh --create \
--topic logs-topic \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1
4️⃣ Launch Pipeline ComponentsRun these in separate terminal tabs:StepComponentCommandALog Generatorpython log_generator/generate_logs.pyBKafka Producerpython kafka_producer/file_producer.pyCPySpark Jobspark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.x.x,org.apache.hadoop:hadoop-aws:3.x.x spark_consumer/spark_etl.py🗃️ Output & ResultsStorage: Data is partitioned and stored in the specified S3 bucket.Format: Parquet (Snappy compressed).Readiness: The data is immediately available for querying via Amazon Athena, AWS Glue, or other Spark sessions.🧠 Key Concepts DemonstratedReal-time Stream Processing: Handling unbounded data with PySpark.Decoupled Architecture: Using Kafka as a message buffer between log production and consumption.Checkpointing: Ensuring fault tolerance in Spark so the pipeline can resume from where it left off.Schema-on-Read: Converting semi-structured logs into a structured relational format.
