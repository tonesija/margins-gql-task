from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.db.database import Base, engine
from app.schema.gql_context import get_context
from app.schema.gql_schema import schema
from app.scripts.seed_sports import seed_sports

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
def init_models():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    seed_sports()


@app.get("/")
async def root():
    return {"message": "Hello World"}
