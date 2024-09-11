# pyrender

## How to install?

### Build wheel file

```shell
docker compose up builder
```

### Install

```shell
pip install dist/<file>.whl
```

## Run

### Init db

```shell
docker compose up -d mysql
docker compose up init_db
```

### Run webserver, worker, scheduler

```shell
docker compose up -d webserver

docker compose up -d redis
docker compose up -d worker
docker compose up -d scheduler
```

## Usage

See `integration` folder for usage.
