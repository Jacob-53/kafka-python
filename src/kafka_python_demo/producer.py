from kafka import KafkaProducer
import time
import json
from tqdm import tqdm

producer = KafkaProducer(
    bootstrap_servers='34.64.249.247:9093',
	value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

batch = 100
for i in tqdm(range(10000)):
	msg = {"msg":str(i)}
	producer.send('jacobgcp_event', msg)
	if (i + 1) % batch == 0:
		producer.flush()
		print(f"flush {i}")
	time.sleep(0.01)
producer.flush()
print("Final flush complete")
