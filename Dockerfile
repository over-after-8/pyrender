FROM python:3.12.4

EXPOSE 5000

WORKDIR /opt/app

RUN apt update \
    && apt install nodejs -y \
    && apt install npm -y

COPY . ./

RUN python setup.py compile_assert install clean

CMD []
