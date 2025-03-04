FROM python:3.12.0-slim-bookworm

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && rm requirements.txt

RUN groupadd -g 1000 appgroup &&  useradd -r -u 1000 -g appgroup app

COPY src ./src

RUN chown -R app:appgroup /app

USER 1000:1000
