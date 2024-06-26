import logging
from functools import reduce
from render.models.job import Job, JobRun
from sqlalchemy.orm import scoped_session

from render.models.user import User
from render.utils.db import provide_session
from croniter import croniter
from datetime import datetime


def max_job_run(job):
    return reduce(lambda r, jr: jr.run_timestamp > r and jr.run_timestamp or r, job.job_runs, job.start)


def get_admin(session: scoped_session = None):
    return session.get(User, 1)


def create_func(func_name_str):
    import importlib
    mod_name, func_name = func_name_str.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    return func


@provide_session
def create_job_runs(session: scoped_session = None):
    admin = get_admin(session)
    jobs = session.query(Job).all()
    max_run_timestamps = [(job, max_job_run(job)) for job in jobs]
    for job, max_job_runs in max_run_timestamps:
        base = max_job_runs
        itr = croniter(str(job.schedule), base)
        next_itr = itr.get_next(datetime)
        while next_itr < job.end:
            job_run = JobRun(job=job, status="new", run_timestamp=next_itr, created_by=1)
            session.add(job_run)
            next_itr = itr.get_next(datetime)


@provide_session
def execute_job_runs(session: scoped_session = None):
    job_runs = session.query(JobRun).filter("new" == JobRun.status).all()
    job_run_tasks = [(job_run.job.task, job_run) for job_run in job_runs]
    for task, job_run in job_run_tasks:
        func = create_func(task)
        func.delay(job_run.id)
        logging.warning(f"Scheduled job run {job_run} for task {task}")
        job_run.status = "scheduled"


@provide_session
def schedule(session: scoped_session = None):
    while True:
        create_job_runs()
        execute_job_runs()


if __name__ == '__main__':
    schedule()
