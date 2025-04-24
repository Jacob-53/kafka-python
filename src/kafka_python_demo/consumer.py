from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'jacobgcp_event',
    bootstrap_servers='34.64.249.247:9093',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='python-consumer-group',
)

print("Listening for messages...\n")

for message in consumer:
    print(f"[RECEIVED] {message.value.decode('utf-8')}")

