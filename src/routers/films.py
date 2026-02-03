from fastapi import APIRouter, Depends, Query

from schemas.types_class import FilmWithCounts, Films, FilmsResponse, FilmsRequest, FilmsWithCountsResponse, PaginatedFilmsResponse, People, Planets, Species, Starships, Vehicles, moviesCharacterAppeared, moviesCharacterAppearedResponse
from services.swapi_services import fetch_by_url, fetch_data, fetch_data_by_id
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

    total = len(result)

    start = (request.page - 1) * request.page_size
    end = start + request.page_size
    paginated = result[start:end]

    response: list[FilmsResponse] = []

    for f in paginated:

        # Characters
        characters = [
            People(name=fetch_by_url(url)["name"])
            for url in f.get("characters", [])
        ]

        # Planets
        planets = []
        for url in f.get("planets", []):
            planet = fetch_by_url(url)
            planets.append(
                Planets(
                    name=planet["name"],
                    population=planet["population"]
                )
            )

        # Starships
        starships = []
        for url in f.get("starships", []):
            ship = fetch_by_url(url)
            pilots = [
                fetch_by_url(pilot)["name"]
                for pilot in ship.get("pilots", [])
            ]
            starships.append(
                Starships(
                    name=ship["name"],
                    model=ship["model"],
                    pilots=pilots
                )
            )

        # Vehicles
        vehicles = []
        for url in f.get("vehicles", []):
            vehicle = fetch_by_url(url)
            vehicles.append(
                Vehicles(
                    name=vehicle["name"],
                    model=vehicle["model"]
                )
            )

        # Species
        species = []
        for url in f.get("species", []):
            specie = fetch_by_url(url)
            species.append(
                Species(
                    name=specie["name"],
                    classification=specie["classification"]
                )
            )

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
                species=species
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


@router.get(
    "/movies_character_appeared",
    response_model=moviesCharacterAppearedResponse
)
def movies_character_appeared(
    name: str | None = Query(None, description="Nome do personagem")
):
    people_data = fetch_data("people")
    films_data = fetch_data("films")

    filters = {}
    if name:
        filters["name"] = name
    
    result = (
        people_data if not filters
        else apply_smart_filters(people_data, filters)
    )

    response = []
    for person in result:
        person_url = person["url"]

        movies = [
            Films(
                title=f["title"],
                director=f["director"]
            )
            for f in films_data
            if person_url in f.get("characters", [])
        ]

        response.append(
            moviesCharacterAppeared(
                name=person["name"],
                movie=movies
            )
        )

    return moviesCharacterAppearedResponse(
        results=response
    )
