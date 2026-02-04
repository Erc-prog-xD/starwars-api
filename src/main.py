from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from services.swapi_services import fetch_data, load_swapi_cache
from utils.filters import apply_filters
from schemas.types_class import Types
from routers.people import router as people_router
from routers.planets import router as planets_router
from routers.films import router as films_router
from routers.starships import router as starships_router
from routers.species import router as species_router
from routers.vehicles import router as vehicles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔹 Carregando cache da SWAPI...")
    load_swapi_cache()
    print("✅ Cache carregado com sucesso")
    yield


app = FastAPI(
    title="Star Wars API",
    description="API para consulta de dados da saga Star Wars usando SWAPI",
    version="1.0.0",
    lifespan=lifespan
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
app.include_router(planets_router)
app.include_router(films_router)
app.include_router(starships_router)
app.include_router(species_router)
app.include_router(vehicles_router)