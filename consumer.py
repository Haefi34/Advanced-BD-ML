
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "transactions_raw",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="consumer_nick",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Waiting for messages...")

count = 0
for message in consumer:
    event = message.value
    print(f"RECEIVED event_id={event['event_id']} "
        f"event_time={event['event_time']} "
        f"real_time={event['event_time_stream']} "
          f"amount={event['amount']} "
          f"label={event['label']}"
    )
    count += 1


consumer.close()
print("Done reading all messages.")

