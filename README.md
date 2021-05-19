# ACCIO

## Getting started

install [docker-compose](https://docs.docker.com/compose/install/)

run `docker-compose up`

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
flask db init
flask db migrate
flask db upgrade
```

to login to accio db:
```
sudo -u postgres psql accio
```