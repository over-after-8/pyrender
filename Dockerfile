FROM node:slim AS node_builder

WORKDIR /opt/app

COPY . ./

RUN cd render/www \
    && npm i \
    && npm run build

CMD []


FROM python:3.12.4 AS render_app

EXPOSE 5000

WORKDIR /opt/app

#RUN apt update \
#    && apt install nodejs -y \
#    && apt install npm -y

RUN pip install build

COPY . ./

COPY --from=node_builder /opt/app/render/www/static/render/dist /opt/app/render/www/static/render/dist

#RUN python setup.py compile_assert install clean

RUN python -m build \
    && pip install dist/render-0.0.1-py3-none-any.whl

CMD []