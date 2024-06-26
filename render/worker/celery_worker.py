from celery import Celery
from sqlalchemy.orm import scoped_session
from render.utils.config import config

from render.models.job import Job

from render.utils.db import provide_session


@provide_session
def get_all_tasks(session: scoped_session = None):
    all_jobs = session.query(Job).all()
    return [".".join(job.task.split(".")[:-1]) for job in all_jobs]


class CeleryWorker:
    celery = None

    def __init__(self, config):
        self.config = config
        if self.celery is None:
            self.celery = Celery(broker=config["celery"]["broker_url"],
                                 backend=config["celery"]["backend_url"],
                                 include=get_all_tasks())

    def get_celery_app(self):
        return self.celery


def worker():
    celery_app = CeleryWorker(config).get_celery_app()
    wk = celery_app.Worker()
    wk.start()


if __name__ == '__main__':
    worker()
