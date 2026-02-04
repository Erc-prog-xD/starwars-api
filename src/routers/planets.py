from fastapi import APIRouter, Depends, Query

from schemas.types_class import Films, PaginatedPlanetsResponse, People, PlanetRequest, PlanetResponse, PopulationStatisticsResponse, TopPlanetsByPopulation, TopPlanetsByResidents
from services.swapi_services import extract_id_from_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters


router = APIRouter(prefix="/planets", tags=["planets"])


@router.get("/by-id/{id}")
def get_planets_by_id(id: int):
    people_data = fetch_data_by_id("planets", id)
    return people_data

@router.get(
    "/list_by_filters",
    response_model=PaginatedPlanetsResponse
)
def list_planets_by_filters(request: PlanetRequest = Depends()):

    planets_data = fetch_data("planets")
    people_data = fetch_data("people")
    films_data = fetch_data("films")

    people_map = {p["url"]: p for p in people_data}
    films_map = {f["url"]: f for f in films_data}

    filters = {}

    if request.name:
        filters["name"] = request.name
    if request.climate:
        filters["climate"] = request.climate
    if request.terrain:
        filters["terrain"] = request.terrain

    result = (
        planets_data if not filters
        else apply_smart_filters(planets_data, filters)
    )

    if request.min_population is not None:
        result = [
            p for p in result
            if p["population"].isdigit()
            and int(p["population"]) >= request.min_population
        ]

    if request.order_by == "url":
        result.sort(
            key=lambda x: extract_id_from_url(x.get("url")),
            reverse=request.order_dir == "desc"
        )
    else:
        result.sort(
            key=lambda x: (x.get(request.order_by) or "").lower(),
            reverse=request.order_dir == "desc"
        )

    total = len(result)
    start = (request.page - 1) * request.page_size
    end = start + request.page_size
    paginated = result[start:end]

    response: list[PlanetResponse] = []

    for p in paginated:

        residents = [
            People(name=people_map[url]["name"])
            for url in p.get("residents", [])
            if url in people_map
        ]

        films = [
            Films(
                title=films_map[url]["title"],
                director=films_map[url]["director"]
            )
            for url in p.get("films", [])
            if url in films_map
        ]

        response.append(
            PlanetResponse(
                name=p["name"],
                rotation_period=p["rotation_period"],
                orbital_period=p["orbital_period"],
                diameter=p["diameter"],
                climate=p["climate"],
                terrain=p["terrain"],
                gravity=p["gravity"],
                population=p["population"],
                surface_water=p["surface_water"],
                residents=residents,
                films=films,
                url_id=p["url"]
            )
        )

    return PaginatedPlanetsResponse(
        page=request.page,
        page_size=request.page_size,
        total=total,
        results=response
    )



@router.get(
    "/population_statistics",
    response_model=PopulationStatisticsResponse
)
def population_statistics():

    data = fetch_data("planets")

    populations = []
    inhabited = 0
    not_inhabited = 0

    for planet in data:
        population = planet.get("population", "")

        if population.isdigit():
            value = int(population)
            populations.append(value)

            if value > 0:
                inhabited += 1
            else:
                not_inhabited += 1
        else:
            not_inhabited += 1

    return PopulationStatisticsResponse(
        total_planets=len(data),
        inhabited=inhabited,
        not_inhabited=not_inhabited,
        avg_population=sum(populations) / len(populations) if populations else 0,
        max_population=max(populations) if populations else 0,
        min_population=min(populations) if populations else 0
    )


@router.get(
    "/top-population",
    response_model=TopPlanetsByPopulation
    
)
def top_planets_by_population():
    data = fetch_data("planets")

    planets = []
    no_population = []

    for p in data:
        population = p.get("population")

        if population and population.isdigit():
            planets.append({
                "name": p["name"],
                "population": int(population)
            })
        else:
            no_population.append({
                "name": p["name"],
                "population": population
            })

    planets.sort(key=lambda x: x["population"], reverse=True)

    return TopPlanetsByPopulation(
        with_population=planets,
        without_population=no_population
    )

@router.get(
    "/top-residents",
    response_model=TopPlanetsByResidents
)
def top_planets_by_residents():
    data = fetch_data("planets")

    planets = [
        {
            "name": p["name"],
            "residents_count": len(p["residents"])
        }
        for p in data
    ]

    planets.sort(key=lambda x: x["residents_count"], reverse=True)

    return {
        "result": planets
    }



