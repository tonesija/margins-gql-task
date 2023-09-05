FROM python:3.11.4-slim as base

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app ./app
COPY .env .env

FROM base as development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

FROM base as test
COPY ./tests ./tests
CMD ["pytest", "-v", "--color=yes"]