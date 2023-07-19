from celery import (
    Celery,
)

BROKER_TRANSPORT_OPTIONS = {
    "region": "us-east-1",
    "polling_interval": 0.3,
    "visibility_timeout": 300,
}
SERVER = Celery(
    "dlq",
    broker=("sqs://"),
    broker_transport_options=BROKER_TRANSPORT_OPTIONS,
    include=["server.tasks"],
    task_default_queue="integrates_streams_dlq",
)

if __name__ == "__main__":
    SERVER.start()
