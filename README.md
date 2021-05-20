# ACCIO

## Getting started

install [docker-compose](https://docs.docker.com/compose/install/)

run `docker-compose up -d`

create virtualenv, activate it and install requirements.
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
source .env
flask run
```

for database migration and setup:
```
flask db migrate
flask db upgrade
```

to login to accio db inside the container:
```
docker-compose exec db bash
psql accio -U postgres
```