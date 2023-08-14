FROM python:3.11-slim-buster

COPY app /application
WORKDIR /application

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

ENV TZ="Europe/Samara"
ENV PYTHONBUFFERED=1
COPY entrypoint.sh /

RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]