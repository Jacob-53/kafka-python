import typer
import json
from kafka import KafkaProducer

def entry_point():
    ip = typer.prompt("Kafka bootstrap_servers 주소를 입력하세요")
    topic = typer.prompt("토픽 이름을 입력하세요")

    broker = f"{ip}:9093"
    producer = KafkaProducer(
        bootstrap_servers=broker,
        value_serializer=lambda v: json.dumps(v,ensure_ascii=False).encode('utf-8')
    )

    typer.echo(f"Kafka 연결됨: {broker} / 토픽: {topic}")
    typer.echo("채팅 시작! (종료하려면 'exit' 입력하세요)\n")

    try:
        while True:
            msg = typer.prompt("You")
            if msg.strip().lower() == "exit":
                typer.echo("채팅 종료합니다!")
                producer.send(topic, msg)
                producer.flush()
                break
            producer.send(topic, msg)
            producer.flush()
    except KeyboardInterrupt:
        typer.echo("\n🛑 채팅 강제 종료")
    finally:
        producer.close()

