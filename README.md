# ACCIO

## Getting started

install postgress:

```
sudo apt-get install postgresql-12
```

login as postgres user
```
sudo -u postgres psql postgres
```
```
CREATE DATABASE accio;
ALTER USER postgres PASSWORD 'postgres';
```
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