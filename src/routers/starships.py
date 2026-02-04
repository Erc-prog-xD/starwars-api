from fastapi import APIRouter, Depends, Query

from schemas.types_class import Films, PaginatedStarshipsResponse, People, StarshipsRequest, StarshipsResponse
from services.swapi_services import extract_id_from_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters


router = APIRouter(prefix="/starships", tags=["starships"])



@router.get("/by-id/{id}")
def get_starships_by_id(id: int):
    starships_data = fetch_data_by_id("starships", id)
    return starships_data

@router.get(
    "/list_starships_by_filters",
    response_model=PaginatedStarshipsResponse
)
def list_starships_by_filters(request: StarshipsRequest = Depends()):

    starships_data = fetch_data("starships")
    people_data = fetch_data("people")
    films_data = fetch_data("films")

    people_map = {p["url"]: p for p in people_data}
    films_map = {f["url"]: f for f in films_data}

    filters = {}

    if request.name:
        filters["name"] = request.name
    if request.model:
        filters["model"] = request.model
    if request.manufacturer:
        filters["manufacturer"] = request.manufacturer
    if request.starship_class:
        filters["starship_class"] = request.starship_class

    result = (
        starships_data if not filters
        else apply_smart_filters(starships_data, filters)
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

    response: list[StarshipsResponse] = []

    for s in paginated:

        pilots = [
            People(name=people_map[url]["name"])
            for url in s.get("pilots", [])
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
            StarshipsResponse(
                name=s["name"],
                model=s["model"],
                manufacturer=s["manufacturer"],
                cost_in_credits=s["cost_in_credits"],
                length=s["length"],
                max_atmosphering_speed=s["max_atmosphering_speed"],
                crew=s["crew"],
                passengers=s["passengers"],
                cargo_capacity=s["cargo_capacity"],
                consumables=s["consumables"],
                hyperdrive_rating=s["hyperdrive_rating"],
                MGLT=s["MGLT"],
                starship_class=s["starship_class"],
                pilots=pilots,
                films=films,
                url_id=s["url"]
            )
        )

    return PaginatedStarshipsResponse(
        page=request.page,
        page_size=request.page_size,
        total=total,
        results=response
    )

@router.get("/stats/overview")
def starships_stats_overview():

    starships = fetch_data("starships")

    total = len(starships)

    class_count = {}
    for s in starships:
        cls = s.get("starship_class")
        if cls:
            class_count[cls] = class_count.get(cls, 0) + 1

    most_common_class = max(class_count, key=class_count.get)
    
    return {
        "total_starships": total,
        "most_common_class": most_common_class,
        "class_distribution": class_count
    }


@router.get("/stats/most_appared_in_movies")
def starships_most_appeared():

    starships = fetch_data("starships")

    result = []

    for s in starships:
        appearances = len(s.get("films", []))
        result.append({
            "name": s["name"],
            "appearances": appearances
        })

    result.sort(key=lambda x: x["appearances"], reverse=True)

    return {
        "results": result
    }



