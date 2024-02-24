import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from pokeapi.dependencies.context import get_context
from pokeapi.presentation.schemas.query import Query

schema = strawberry.Schema(Query)
graphql_app: GraphQLRouter = GraphQLRouter(
    schema, context_getter=get_context, path="/graphql"
)

app = FastAPI()
app.include_router(graphql_app)


@app.get("/health")
def health_check() -> dict:
    return {"status": "OK"}
