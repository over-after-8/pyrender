docker-up:
    docker-compose up --build -d

version:
    docker-compose run --rm webserver urd version

docker-build:
    docker build -t urd:0.0.1 .

docker-down:
    docker-compose down

db_init:
    docker-compose run --rm webserver urd db_init

yarn-build:
    cd ui_render/www && yarn install --from-lock-file && yarn run build

yarn-start:
    cd ui_render/www && yarn install --from-lock-file && yarn run start

install:
    pip uninstall ui_render -y
    python setup.py bdist_wheel && pip install dist/ui_render-0.0.1-py3-none-any.whl --force-reinstall && python setup.py clean
