### Task for Valere Margins interview process

App is written in Python, using FastAPI framework and Strawberry for GraphQL API.

#### Starting the app

##### Without docker compose

Setup (create virtual environment, install deps)

- pyton3 -m venv. venv
- source .venv/bin/activate
- pip install -r requirements
- copy and rename .env.example to .env and insert your values

Database can be created and started with Docker:

- docker run --name postgres-margins -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=Margins -p 5432:5432 -d postgres

Running the app:

- Prerequisites:
  - in venv
  - database started
- uvicorn app.main:app --reload

Running tests

- Prerequisites:
  - in venv
  - database started
- pytest -v

##### With docker compose

#### Would be nice to have

Many features and improvements have been identified during the development, but due to the time constraint and the main goal of this excercise being appraisal of candidate's ability in software development and his opportunity to learn about GraphQL, they were left out.

- database migrations with **alembic**
- more complete unit and integration tests with **pytest**, along with TDD approach for developing the app
- cleaner **arrange** step in tests

#### Notes:

Email verification is functional, however user will still be authorized if he's not verified. This has been done on purpose for easier demonstration, and the step to enable that authorization is trivial.
