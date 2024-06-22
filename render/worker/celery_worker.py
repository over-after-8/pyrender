from celery import Celery


class CeleryWorker:
    celery = None

    def __init__(self, config):
        self.config = config
        if self.celery is None:
            self.celery = Celery(broker=config["celery"]["broker_url"],
                                 backend=config["celery"]["backend_url"],
                                 include=["render.worker.tasks"])

    def get_celery_app(self):
        return self.celery
