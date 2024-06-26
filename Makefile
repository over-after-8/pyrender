docker-up:
	docker compose up --build -d

version:
	docker compose run --rm webserver render version

docker-build:
	docker build -t pyrender:0.0.1 .

docker-down:
	docker compose down

db_init:
	docker compose run --rm webserver render db_init

npm-build:
	cd render/www && npm i --from-lock-file && npm run build

npm-start:
	cd render/www && npm install --from-lock-file && npm run start

install:
	pip uninstall render -y
	python setup.py bdist_wheel && pip install dist/render-0.0.1-py3-none-any.whl --force-reinstall && python setup.py clean
