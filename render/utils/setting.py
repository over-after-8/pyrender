from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from render.utils.config import config

mysql_config = config["mysql"]
mysql_engine = None
mysql_session = None


def configure_validation_session():
    global mysql_session
    global mysql_config
    global mysql_engine
    mysql_engine = create_engine(mysql_config["sql_alchemy_conn"], echo=False)

    mysql_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=mysql_engine,
            expire_on_commit=False
        )
    )


def initialize():
    configure_validation_session()


initialize()
