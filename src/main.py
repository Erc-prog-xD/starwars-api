from fastapi import FastAPI, Query
from services.swapi_services import fetch_data
from utils.filters import apply_filters
from schemas.types_class import Types
from routers.people import router as people_router
from routers.planets import router as planets_router
from routers.films import router as films_router
from routers.starships import router as starships_router
from routers.species import router as species_router
from routers.vehicles import router as vehicles_router


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

from fastapi import FastAPI
from services.swapi_services import fetch_data, fetch_by_url
import logging

app = FastAPI(
    title="Star Wars API",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)


# @app.on_event("startup")
# def warm_up_cache():
#     resources = [
#         "people",
#         "films",
#         "planets",
#         "species",
#         "vehicles",
#         "starships"
#     ]

#     logging.info("🔄 Iniciando warm-up do cache SWAPI...")

#     for resource in resources:
#         data = fetch_data(resource)

#         for item in data:
#             fetch_by_url(item["url"])

#             for field in [
#                 "films",
#                 "characters",
#                 "people",
#                 "residents",
#                 "species",
#                 "vehicles",
#                 "starships",
#                 "pilots"
#             ]:
#                 for url in item.get(field, []):
#                     fetch_by_url(url)

#     logging.info("✅ Cache aquecido com sucesso!")


app.include_router(people_router)
app.include_router(planets_router)
app.include_router(films_router)
app.include_router(starships_router)
app.include_router(species_router)
app.include_router(vehicles_router)