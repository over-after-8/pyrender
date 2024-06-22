from render.utils.config import config
from render.worker.celery_worker import CeleryWorker

app = CeleryWorker(config).get_celery_app()


@app.task
def add():
    return 10 + 20
