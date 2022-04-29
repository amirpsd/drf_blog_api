FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir src/
WORKDIR /src
ADD ./src /src 

# install dependencies
RUN pip3 install --upgrade pip
ADD ./requirements /requirements
RUN pip3 install -r /requirements/production.txt

CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    gunicorn -b 0.0.0.0:8000 config.wsgi