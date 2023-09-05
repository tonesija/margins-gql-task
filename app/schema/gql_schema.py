import strawberry

from app.schema.gql_context import SQLAlchemySession
from app.schema.mutation_schema import Mutation
from app.schema.query_schema import Query

schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[SQLAlchemySession]
)
