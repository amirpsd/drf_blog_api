# Django Blog Api

![Django Rest Framework](src/static/django_rest_framework.png)

This project is a Blog site written with [python3.9](https://www.python.org) and
[Django3.2](https://docs.djangoproject.com/en/3.2/releases/3.2/) and 
[Django_rest_framework_3.12](https://www.django-rest-framework.org) which is for using api.

# Setup

### Clone the project

```shell
git clone https://github.com/amirpsd/django_blog_api.git && cd django_blog_api && cp .env-sample .env && cp .env.db-example .env.db && rm .env-sample .env.db-example
```

### install Docker

You must install Docker.

- [install in Linux](https://docs.docker.com/engine/install/)
- [install in Windows](https://docs.docker.com/desktop/windows/install/)
- [install in Mac](https://docs.docker.com/desktop/mac/install/)

### Run project

create docker network

```shell
docker network create nginx_network1
docker network create blog_network
```

create docker volume

```shell
docker volume create db_data
```

run project

```shell
docker-compose up -d
```

### LICENSE

see the [LICENSE](https://github.com/amirpsd/django_blog_api/blob/main/LICENSE) file for details
