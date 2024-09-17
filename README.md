# Social media API
This project is a Django REST API for managing a social media simple 
operations including creating, adding, deleting profile, following and unfollowing 
users, creating and observing posts. 
The project is containerized using Docker and includes automatic API documentation 
with Swagger and Redoc.

## Installing using GitHub

Install PostgreSQL and create db

- git clone https://github.com/MykhailoIvchenko/social-media-api.git
- cd social-media-api
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- set POSTGRES_HOST=<your db hostname>
- set POSTGRES_DB=<your db name>
- set POSTGRES_USER=<your db username>
- set POSTGRES_PASSWORD=<your db user password>
- set PGDATA=<your link to the pg data>
- set SECRET_KEY=<your secret key>
- `python manage.py migrate`
- `python manage.py runserver`

## Run with Docker (recommended way)

Install [Docker Desktop](https://docs.docker.com/desktop/) and launch it

- `docker-compose build`
- `docker-compose up`

## Getting access

- create user via /api/user/register
- get access token via /api/user/token

## Getting access as admin
- enter container docker exec -it <container_name> sh, 
- create superuser by the command `python manage.py createsuperuser`

## Features
- JWT authenticated
- Admin panel /admin/
- Documentation is located at api/doc/swagger of at api/doc/redoc
- Creating user profile
- Updating your own profile
- Deleting your own profile
- Following/unfollowing other users
- Creating posts
- Watching own posts and posts of followed users

