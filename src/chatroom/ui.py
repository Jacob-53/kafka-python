from textual.app import App, ComposeResult
from textual.widgets import TextArea, Input, Button, Static
from textual.containers import Vertical
from kafka import KafkaConsumer, KafkaProducer
import json
import threading


class KafkaChatApp(App):
    BINDINGS = [("ctrl+c", "quit", "앱 종료"), ("escape", "quit", "앱 종료")]

    def __init__(self):
        super().__init__()
        self.broker = ""
        self.topic = ""
        self.my_name = ""
        self.consumer = None
        self.producer = None
        self.chat_log = None

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("💬 Kafka 채팅 시작", id="title")
            yield Input(placeholder="📡 Kafka broker (예: 34.64.x.x:9093)", id="broker")
            yield Input(placeholder="💬 채팅 토픽", id="topic")
            yield Input(placeholder="🧑 내 이름", id="name")
            yield Button("✅ 채팅 시작", id="start")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "start":
            self.broker = self.query_one("#broker", Input).value.strip()
            self.topic = self.query_one("#topic", Input).value.strip()
            self.my_name = self.query_one("#name", Input).value.strip()

            # 입력 폼 제거
            self.query_one("#title").remove()
            self.query_one("#broker").remove()
            self.query_one("#topic").remove()
            self.query_one("#name").remove()
            event.button.remove()

            # 채팅창 UI 구성
            self.chat_log = TextArea()
            self.chat_log.disabled = True
            self.mount(self.chat_log)
            self.mount(Input(placeholder="메시지를 입력하세요... (exit 입력 시 종료)", id="chat-input"))

            # Kafka 연결
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.broker,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                group_id=f"chat-{self.my_name}"
            )

            self.producer = KafkaProducer(
                bootstrap_servers=self.broker,
                value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8")
            )

            # 메시지 수신 쓰레드 시작
            threading.Thread(target=self.consume_loop, daemon=True).start()

    def consume_loop(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode("utf-8"))
                sender = data.get("sender")
                message = data.get("message")
                if sender != self.my_name:
                    self.call_from_thread(lambda: self.append_message(f"{sender} > {message}"))
            except Exception as e:
                self.call_from_thread(lambda: self.append_message(f"❌ JSON 오류: {e}"))

    def append_message(self, message: str):
        if self.chat_log:
            self.chat_log.text += f"{message}\n"

    async def on_input_submitted(self, event: Input.Submitted):
        msg = event.value.strip()
        if msg.lower() == "exit":
            self.append_message("👋 종료 명령 감지됨, 채팅 앱 종료 중...")
            await self.action_quit()
            return

        self.append_message(f"{self.my_name} > {msg}")
        self.producer.send(self.topic, {"sender": self.my_name, "message": msg})
        self.producer.flush()
        event.input.value = ""

    def on_exit(self) -> None:
        if self.producer:
            self.producer.close()


def entry_point():
    app = KafkaChatApp()
    app.run()


if __name__ == "__main__":
    entry_point()

