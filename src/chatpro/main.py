# chatpro.py
import typer
import json
from kafka import KafkaProducer

def entry_point():
    ip = typer.prompt("📡 Kafka bootstrap_servers 주소를 입력하세요")
    topic = typer.prompt("💬 토픽 이름을 입력하세요")

    broker = f"{ip}:9093"
    producer = KafkaProducer(
        bootstrap_servers=broker,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    typer.echo(f"✅ Kafka 연결됨: {broker} / 토픽: {topic}")
    typer.echo("✉️ 채팅 시작! (Ctrl+C로 종료)\n")

    try:
        while True:
            msg = typer.prompt("You")
            producer.send(topic, msg)
            producer.flush()
    except KeyboardInterrupt:
        typer.echo("\n🛑 채팅 종료")
        producer.close()

