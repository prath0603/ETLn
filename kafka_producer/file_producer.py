from kafka import KafkaProducer
import time
import os
import json

# =========================
# Paths and topic
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(DATA_FOLDER, "app.log")
OFFSET_FILE = os.path.join(DATA_FOLDER, "app.log.offset")
TOPIC = "log-topic"

os.makedirs(DATA_FOLDER, exist_ok=True)

# =========================
# Kafka Producer
# =========================
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =========================
# Offset helpers
# =========================
def read_last_offset():
    """Read last processed file offset"""
    if os.path.isfile(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as f:
            val = f.read().strip()
            return int(val) if val.isdigit() else 0
    return 0

def save_offset(offset):
    """Save current file offset"""
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))

# =========================
# Tail file and send to Kafka
# =========================
def tail_file(file_path):
    """Continuously tail a file and send new lines to Kafka"""
    print(f"Kafka producer waiting for logs in {file_path}...")

    last_offset = read_last_offset()

    while True:
        if not os.path.isfile(file_path):
            time.sleep(1)
            continue

        with open(file_path, "r", buffering=1) as f:  # line-buffered mode
            f.seek(last_offset, os.SEEK_SET)

            while True:
                line = f.readline()
                if not line:
                    # End of file, wait for new lines
                    time.sleep(0.2)
                    continue

                line = line.strip()
                if not line:
                    save_offset(f.tell())
                    continue

                # Wrap log line in JSON
                log_json = {"log_line": line}
                try:
                    producer.send(TOPIC, log_json)
                    producer.flush()
                    print("Sent to Kafka:", log_json)
                except Exception as e:
                    print("Error sending to Kafka:", e)

                # Save offset after successful send
                save_offset(f.tell())

# =========================
# Main
# =========================
if __name__ == "__main__":
    try:
        tail_file(LOG_FILE)
    except KeyboardInterrupt:
        print("\nStopping producer...")
