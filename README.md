# members-app-backend 

## Installation 

#### Docker First installation
Edit /src/CSI/settings.py and add SECRET_KEY
```
docker-compose build
```

To start
```
docker-compose up -d
```
Collect static
```
docker exec dg01 /bin/sh -c "python3 manage.py collectstatic --noinput"  
```

To stop
```
docker-compose stop
```

#### Alternative Method

Install PostgreSQL

Create a user,database

Install modules from requirement.txt

Rename settings_dummy.py to settings.py

Add secret key

Update database details

Migrate

Collect Static

Configure Nginx and gunicorn

## Api documentation

Documentation can be found at
http://docs.csimem.apiary.io
