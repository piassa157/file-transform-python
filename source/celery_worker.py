import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

broker_url = os.getenv("CELERY_BROKER_URL")


app = Celery(
    'api-project',
    broker=broker_url,
    backend='rpc://',
    include=['tasks']
)

if __name__ == '__main__':
    app.start()