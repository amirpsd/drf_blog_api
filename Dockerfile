FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

RUN mkdir src/
WORKDIR /src
ADD ./src /src 

# install dependencies
RUN pip3 install --upgrade pip
ADD ./requirements/requirements.txt /src
RUN pip3 install -r requirements.txt

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 2 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@gmail.com --noinput; \
    gunicorn -b 0.0.0.0:8000 config.wsgi