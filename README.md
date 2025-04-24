# kafka-python 수련
## 📨 Kafka CLI Chat - Typer 기반 채팅 툴

Typer + Kafka + PDM을 기반으로 만든 **Kafka CLI 채팅 도구**입니다.  
간단한 명령어만으로 Kafka 브로커와 연결해 실시간 메시지를 주고받을 수 있습니다.

## ✨ 주요 기능
- Kafka Producer CLI 실행 (`pdm run chatpro`, bashrc에 alias 등록시 `chatpro` ,`chatcon` 명령으로 실행 가능 )
  - < alias chatpro="/<사용자경로>/.venv/bin/chatpro" >
  - < alias chatcon="/<사용자경로>/.venv/bin/chatcon" >
- IP와 토픽을 프롬프트에서 입력
- 실시간 메시지 입력 → Kafka로 전송
- `exit` 입력 또는 `Ctrl+C`로 종료
- PDM으로 의존성 및 스크립트 관리

## 실행 예시
```bash
$ source .venv/bin/activate
$ pdm install
```
- producer
```bash
$ chatpro
Kafka bootstrap_servers 주소를 입력하세요: 3.36.124.60
토픽 이름을 입력하세요: chatroom
Kafka 연결됨: 3.36.124.60:9093 / 토픽: chatroom
채팅 시작! (종료하려면 'exit' 입력 또는 Ctrl+C)

You > 안녕하세요!
You > exit
채팅 종료합니다!
```

- consumer
```bash
$ chatcon
Kafka bootstrap_servers 주소를 입력하세요: 3.36.124.60
토픽 이름을 입력하세요: chatroom

[2025-04-24 15:43:10] Friend > 안녕하세요!
[2025-04-24 15:43:13] Friend > exit
상대가 채팅을 종료했습니다.
```


## 파일 구조
```bash
kafka-python-demo/
├── pyproject.toml
├── README.md
└── src/
    ├── chatpro/
    │   ├── __init__.py
    │   └── main.py   # 메시지 전송
    └── chatcon/
        ├── __init__.py
        └── main.py   # 메시지 수신
```
