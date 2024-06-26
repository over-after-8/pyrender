import logging

from render.models.job import JobRun
from sqlalchemy.orm import scoped_session

from render.utils.config import config
from render.utils.db import provide_session
from render.worker.celery_worker import CeleryWorker
import time

app = CeleryWorker(config).get_celery_app()


def update_job_run(func):
    @provide_session
    def update(job_run_id, status, session: scoped_session = None):
        job_run = session.get(JobRun, job_run_id)
        job_run.status = status

    def wrapper(job_run_id, *args, **kwargs):
        try:
            logging.info(f"Running {func.__name__}; job run {job_run_id}")
            func(*args, **kwargs)
            status = "done"
            logging.info(f"Finished {func.__name__}; job run {job_run_id}")
        except Exception as e:
            logging.error(e)
            status = "failed"
            logging.error(f"Failed {func.__name__}; job run {job_run_id}")
        update(job_run_id, status)

    return wrapper


@app.task
@update_job_run
def add():
    time.sleep(1)
    return 10 + 20
