from typing import List

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from render.utils.base import Base, basic_fields


@basic_fields
class Job(Base):
    __tablename__ = 'jobs'

    id = mapped_column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(63), nullable=False)
    task = Column(String(255), nullable=False)
    start = Column(TIMESTAMP, nullable=False)
    end = Column(TIMESTAMP, nullable=True)
    schedule = Column(String(63), nullable=False)
    job_runs: Mapped[List["JobRun"]] = relationship(back_populates="job")

    def __repr__(self):
        return 'Job(id={self.id}, name={self.name})'.format(self=self)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "task": self.task,
            "schedule": self.schedule,
            "start": self.start,
            "end": self.end
        }


@basic_fields
class JobRun(Base):
    __tablename__ = 'job_runs'

    id = mapped_column(BigInteger, primary_key=True, nullable=False)
    job_id = Column(BigInteger, ForeignKey('jobs.id'), nullable=False)
    status = Column(String(15), nullable=False)
    run_timestamp = Column(TIMESTAMP, nullable=False)
    job: Mapped["Job"] = relationship(back_populates="job_runs")

    def __repr__(self):
        return '<JonRun(job_id={}, run={})>'.format(self.job_id, self.run_timestamp)

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'status': self.status,
            'run_timestamp': self.run_timestamp,
            "job": self.job.to_dict()
        }
