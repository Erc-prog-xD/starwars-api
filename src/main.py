from fastapi import FastAPI, Query
from services.swapi_services import fetch_data
from utils.filters import apply_filters
from schemas.types_class import Types
from routers.people import router as people_router


app = FastAPI(
    title="Star Wars API",
    description="API para consulta de dados da saga Star Wars usando SWAPI",
    version="1.0.0"
)


@app.get("/")
def get_data(
    type: Types = Query(..., description="Tipo de recurso da SWAPI"),
    name: str | None = Query(None, description="Filtro por nome")
):
    data = fetch_data(type.value)

    filters = {}

    if name:
        if type.value == "films":
            filters["title"] = name
        else: 
            filters["name"] = name

    result = apply_filters(data, filters)
    return {"results": result}

app.include_router(people_router)