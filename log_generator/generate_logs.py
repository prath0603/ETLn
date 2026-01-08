import time
import random
from datetime import datetime
import os
# Absolute path to logs folder (works regardless of current directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FOLDER = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(LOG_FOLDER, "app.log")
# Create folder automatically if missing
os.makedirs(LOG_FOLDER, exist_ok=True)
def generate_log():
    sno = 1
    # Resume SNO if file exists
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                if last_line.startswith("SNO="):
                    sno = int(last_line.split("=")[1].split(" ")[0]) + 1
    while True:
        log_line = (
            f"SNO={sno} | "
            f"{datetime.now()} | INFO | "
            f"request_id={random.randint(1,999)} | "
            f"user_id={random.randint(1,200)} | "
            f"response_time={random.randint(10,600)} | "
            f"status=200"
        )
        # Append log to file
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
        # Optional: print to terminal for debugging (can comment out)
        print("Generated:", log_line)
        sno += 1
        time.sleep(1)
if __name__ == "__main__":
    generate_log()