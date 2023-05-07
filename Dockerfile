FROM python:3.10-alpine
WORKDIR /posttgbot

LABEL authors="Kachu"

RUN pip install --upgrade pip && \
pip install poetry

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:./bot"

COPY pyproject.toml .
COPY bot ./bot

RUN poetry install

CMD ["poetry", "run", "python", "-m", "bot"]