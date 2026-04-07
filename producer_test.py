import json
import os
import time

import kagglehub
import pandas as pd
from kafka import KafkaProducer
from datetime import datetime, timedelta

SPEEDUP = 100
MAX_EVENTS = 300000

path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
csv_path = os.path.join(path, "creditcard.csv")

df = pd.read_csv(csv_path)
df = df.sort_values("Time").reset_index(drop=True)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

prev_time = None

start_time = datetime.now()

for i, row in df.iterrows():
    current_time = float(row["Time"])
    event_time_stream = start_time + timedelta(seconds=current_time)

    if prev_time is not None:
        delay = (current_time - prev_time) / SPEEDUP
        if delay > 0:
            time.sleep(delay)


    event = {
        "event_id": int(i),
        "event_time": current_time,
        "event_time_stream": event_time_stream.isoformat(),
        "amount": float(row["Amount"]),
        "features": [float(row[f"V{j}"]) for j in range(1, 29)],
        "label": int(row["Class"])
    }

    producer.send("transactions_raw", event)
    print(f"sent event_id={event['event_id']} event_time={event['event_time']} event_time_stream={event['event_time_stream']} amount={event['amount']}")

    prev_time = current_time

producer.flush()
print("Done streaming.")
