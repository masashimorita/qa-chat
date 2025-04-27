FROM python:3.11

RUN apt-get -y update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_IN_PROJECT 1

WORKDIR /app

RUN pip install poetry

COPY . /app

# Set the entrypoint to use poetry
ENTRYPOINT ["poetry", "run"]
