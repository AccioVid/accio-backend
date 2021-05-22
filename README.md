# ACCIO

## Getting started

install [docker-compose](https://docs.docker.com/compose/install/)

first time setup
```bash
docker-compose up -d
scripts/init.sh
pip install -r requirements.txt
```



for database migration and setup:
```bash
flask db migrate
flask db upgrade
```

to login to accio db inside the container:
```
docker-compose exec db bash
psql accio -U postgres
```

run the server

```bash
flask run
```


