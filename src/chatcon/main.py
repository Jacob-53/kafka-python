import typer
from kafka import KafkaConsumer
from datetime import datetime

def entry_point():
    ip = typer.prompt("Kafka bootstrap_servers 주소를 입력하세요")
    topic = typer.prompt("토픽 이름을 입력하세요")

    broker = f"{ip}:9093"
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id="chatcli-consumer"
    )

    typer.echo(f"Kafka 연결됨: {broker} / 토픽: {topic}")
    typer.echo("메시지 수신 대기 중... (종료하려면 'exit' 입력 또는 Ctrl+C)\n")

    try:
        while True:
            for message in consumer:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                decoded = message.value.decode('utf-8')
                if decoded.strip().lower() == "exit":
                    typer.echo("상대가 채팅을 종료했습니다.")
                    return
                typer.echo(f"[{now}] Friend > {decoded}")
    except KeyboardInterrupt:
        typer.echo("\n🛑 수신 강제 종료")
    finally:
        consumer.close()

