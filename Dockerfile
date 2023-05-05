FROM python:3.10-alpine
WORKDIR /posttgbot

LABEL authors="Kachu"

COPY pyproject.toml .
COPY bot ./bot

RUN pip install poetry
RUN poetry install

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:./bot"

CMD poetry run python -m bot