from celery import shared_task
import time

@shared_task
def ping(message="pong"):
    time.sleep(1)
    return f"PONG: {message}"
