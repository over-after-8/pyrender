from celery import Celery


class CeleryWorker:
    def __init__(self, config):
        self.config = config
        self.celery = Celery(config["celery"]["app_name"], broker=config["celery"]["broker_url"],
                             backend=config["celery"]["backend_url"])

    def get_celery_app(self):
        return self.celery
