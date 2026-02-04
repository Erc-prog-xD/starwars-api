from fastapi import APIRouter, Depends, Query

from schemas.types_class import FilmWithCounts, FilmsResponse, FilmsRequest, FilmsWithCountsResponse, PaginatedFilmsResponse, People, Planets, Species, Starships, Vehicles
from services.swapi_services import extract_id_from_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters


router = APIRouter(prefix="/films", tags=["films"])



@router.get("/by-id/{id}")
def get_films_by_id(id: int):
    film_data = fetch_data_by_id("films", id)
    return film_data



@router.get(
    "/list_by_filters",
    response_model=PaginatedFilmsResponse
)
def list_films_by_filters(request: FilmsRequest = Depends()):

    films_data = fetch_data("films")
    people_data = fetch_data("people")
    species_data = fetch_data("species")
    vehicles_data = fetch_data("vehicles")
    starships_data = fetch_data("starships")
    planets_data = fetch_data("planets")

    # 🔹 mapas por URL (lookup O(1))
    people_map = {p["url"]: p for p in people_data}
    species_map = {s["url"]: s for s in species_data}
    vehicles_map = {v["url"]: v for v in vehicles_data}
    starships_map = {s["url"]: s for s in starships_data}
    planets_map = {p["url"]: p for p in planets_data}

    filters = {}

    if request.title:
        filters["title"] = request.title
    if request.director:
        filters["director"] = request.director
    if request.producer:
        filters["producer"] = request.producer
    if request.episode_id:
        filters["episode_id"] = request.episode_id
    if request.release_date:
        filters["release_date"] = request.release_date.isoformat()

    result = (
        films_data if not filters
        else apply_smart_filters(films_data, filters)
    )

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

    response: list[FilmsResponse] = []

    for f in paginated:

        # 👤 Characters
        characters = [
            People(name=people_map[url]["name"])
            for url in f.get("characters", [])
            if url in people_map
        ]

        # 🌍 Planets
        planets = [
            Planets(
                name=planets_map[url]["name"],
                population=planets_map[url]["population"]
            )
            for url in f.get("planets", [])
            if url in planets_map
        ]

        # 🚀 Starships
        starships = []
        for url in f.get("starships", []):
            if url not in starships_map:
                continue

            ship = starships_map[url]
            pilots = [
                people_map[pilot]["name"]
                for pilot in ship.get("pilots", [])
                if pilot in people_map
            ]

            starships.append(
                Starships(
                    name=ship["name"],
                    model=ship["model"],
                    pilots=pilots
                )
            )

        # 🚗 Vehicles
        vehicles = [
            Vehicles(
                name=vehicles_map[url]["name"],
                model=vehicles_map[url]["model"]
            )
            for url in f.get("vehicles", [])
            if url in vehicles_map
        ]

        # 🧬 Species
        species = [
            Species(
                name=species_map[url]["name"],
                classification=species_map[url]["classification"]
            )
            for url in f.get("species", [])
            if url in species_map
        ]

        response.append(
            FilmsResponse(
                title=f["title"],
                episode_id=f["episode_id"],
                opening_crawl=f["opening_crawl"],
                director=f["director"],
                producer=f["producer"],
                release_date=f["release_date"],
                characters=characters,
                planets=planets,
                starships=starships,
                vehicles=vehicles,
                species=species,
                url_id=f["url"]
            )
        )

    return PaginatedFilmsResponse(
        page=request.page,
        page_size=request.page_size,
        total=total,
        results=response
    )


@router.get(
    "/list_with_counts",
    response_model=FilmsWithCountsResponse
)
def list_films_with_counts():

    films_data = fetch_data("films")

    results = [
        FilmWithCounts(
            title = f.get("title"),
            characters_count=len(f.get("characters", [])),
            planets_count=len(f.get("planets", [])),
            starships_count=len(f.get("starships", [])),
            vehicles_count=len(f.get("vehicles", [])),
            species_count=len(f.get("species", []))
        )
        for f in films_data
    ]

    return FilmsWithCountsResponse(results=results)



