from fastapi import APIRouter, Depends, Query

from schemas.types_class import Films, PaginatedSpeciesResponse, People, SpeciesRequest, SpeciesResponse
from services.swapi_services import extract_id_from_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters, safe_int




router = APIRouter(prefix="/species", tags=["species"])

@router.get("/by-id/{id}")
def get_species_by_id(id: int):
    species_data = fetch_data_by_id("species", id)
    return species_data




@router.get(
    "/list_species_by_filters",
    response_model=PaginatedSpeciesResponse
)
def list_species_by_filters(request: SpeciesRequest = Depends()):

    species_data = fetch_data("species")
    people_data = fetch_data("people")
    films_data = fetch_data("films")
    planets_data = fetch_data("planets")

    people_map = {p["url"]: p for p in people_data}
    films_map = {f["url"]: f for f in films_data}
    planets_map = {p["url"]: p for p in planets_data}

    filters = {}

    if request.name:
        filters["name"] = request.name
    if request.classification:
        filters["classification"] = request.classification
    if request.designation:
        filters["designation"] = request.designation
    if request.language:
        filters["language"] = request.language

    result = (
        species_data if not filters
        else apply_smart_filters(species_data, filters)
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

    response: list[SpeciesResponse] = []

    for s in paginated:

        
        homeworld = None
        if s.get("homeworld") in planets_map:
            homeworld = planets_map[s["homeworld"]]["name"]

        people = [
            People(name=people_map[url]["name"])
            for url in s.get("people", [])
            if url in people_map
        ]

        films = [
            Films(
                title=films_map[url]["title"],
                director=films_map[url]["director"]
            )
            for url in s.get("films", [])
            if url in films_map
        ]

        response.append(
            SpeciesResponse(
                name=s["name"],
                classification=s["classification"],
                designation=s["designation"],
                average_height=s["average_height"],
                skin_colors=s["skin_colors"],
                hair_colors=s["hair_colors"],
                eye_colors=s["eye_colors"],
                average_lifespan=s["average_lifespan"],
                homeworld=homeworld, 
                language=s["language"],
                people=people,
                films=films,
                url_id=s["url"]
            )
        )

    return PaginatedSpeciesResponse(
        page=request.page,
        page_size=request.page_size,
        total=total,
        results=response
    )


@router.get("/stats/overview")
def species_stats_overview():

    species = fetch_data("species")

    total = len(species)

    classifications = {}
    designations = {}

    for s in species:
        if s.get("classification"):
            classifications[s["classification"]] = classifications.get(s["classification"], 0) + 1

        if s.get("designation"):
            designations[s["designation"]] = designations.get(s["designation"], 0) + 1

    return {
        "total_species": total,
        "classifications": classifications,
        "designations": designations
    }


@router.get("/stats/height")
def species_height_stats():

    species = fetch_data("species")

    heights = []

    tallest = None
    max_height = 0

    for s in species:
        height = safe_int(s.get("average_height", ""))
        if height is not None:
            heights.append(height)

            if height > max_height:
                max_height = height
                tallest = {
                    "name": s["name"],
                    "average_height": height
                }

    avg_height = sum(heights) / len(heights) if heights else 0

    return {
        "average_height": round(avg_height, 2),
        "tallest_species": tallest
    }


@router.get("/stats/lifespan")
def species_lifespan_stats():

    species = fetch_data("species")

    lifespans = []

    longest_living = None
    max_lifespan = 0

    for s in species:
        lifespan = safe_int(s.get("average_lifespan", ""))
        if lifespan is not None:
            lifespans.append(lifespan)

            if lifespan > max_lifespan:
                max_lifespan = lifespan
                longest_living = {
                    "name": s["name"],
                    "average_lifespan": lifespan
                }

    avg_lifespan = sum(lifespans) / len(lifespans) if lifespans else 0

    return {
        "average_lifespan": round(avg_lifespan, 2),
        "longest_living_species": longest_living
    }


@router.get("/stats/most_appeared_in_movies")
def most_appeared_in_movies():

    species = fetch_data("species")

    result = []

    for s in species:
        result.append({
            "name": s["name"],
            "appearances": len(s.get("films", []))
        })

    result.sort(key=lambda x: x["appearances"], reverse=True)

    return {
        "results": result
    }


@router.get("/stats/people")
def species_people_stats():

    species = fetch_data("species")

    result = []

    for s in species:
        result.append({
            "name": s["name"],
            "total_people": len(s.get("people", []))
        })

    result.sort(key=lambda x: x["total_people"], reverse=True)

    return {
        "results": result
    }


@router.get("/stats/language")
def species_language_stats():

    species = fetch_data("species")

    languages = {}

    for s in species:
        lang = s.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    return {
        "languages": languages
    }
