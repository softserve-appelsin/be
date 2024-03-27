# SoftServe FECT LNU 2024 - Backend
Python + Django

## Run localy

```sh
docker-compose -f docker-compose.yml up -d --build
```

### with postgres
```sh
docker-compose -f docker-compose.postgres.yml up -d
```
On first run postgres db will be created, wich will be reused on next run. 

! Warning

If for some reason you need to delete db data, run next command:
```sh
docker-compose -f docker-compose.postgres.yml stop
docker-compose -f docker-compose.postgres.yml down -v
```


Backend will be running on [localhost:8000](http://127.0.0.1:8000). For local development [sqlite-db](./db.sqlite3) is used.

## Run in Cloud
