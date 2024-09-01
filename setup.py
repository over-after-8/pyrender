import os
from pathlib import Path

from setuptools import setup

name = "render"
version = "0.0.1"
SOURCES_ROOT = Path(__file__).parent.resolve()


def do_setup():
    packages = [x[0].replace("./", "").replace("/", ".") for x in
                filter(lambda x: x[2].__contains__("__init__.py"), os.walk("./"))]

    setup(
        name=name,
        version=version,
        packages=packages,
        include_package_data=True,
        license="MIT",
        author="ManhDoi",
        install_requires=["importlib_metadata==7.1.0",
                          "celery",
                          "celery[redis]",
                          "mysqlclient==2.2.4",
                          "Flask-SQLAlchemy==3.1.1",
                          "Flask-WTF==1.2.1",
                          "croniter==2.0.5",
                          "Flask-Login==0.6.3"],
        cmdclass={}
    )


if __name__ == '__main__':
    do_setup()
