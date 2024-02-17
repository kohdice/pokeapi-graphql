import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from pokeapi.presentation.schemas.query import Query

schema = strawberry.Schema(Query)
graphql_app: GraphQLRouter = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
def health_check() -> dict:
    return {"status": "OK"}
