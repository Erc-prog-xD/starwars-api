from fastapi import APIRouter, Depends, Query

from schemas.types_class import Films, PaginatedStarshipsResponse, People, StarshipsRequest, StarshipsResponse
from services.swapi_services import extract_id_from_url, fetch_by_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters


router = APIRouter(prefix="/starships", tags=["starships"])



@router.get("/by-id/{id}")
def get_starships_by_id(id: int):
    starships_data = fetch_data_by_id("starships", id)
    return starships_data

@router.get(
    "/list_by_filters",
    response_model=PaginatedStarshipsResponse
)
def list_starships_by_filters(request: StarshipsRequest = Depends()):

    starships_data = fetch_data("starships")

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
    print(request.order_dir)

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

        # Pilots
        pilots = [
            People(name=fetch_by_url(url)["name"])
            for url in s.get("pilots", [])
        ]

        # Films
        films = [
            Films(
                title=fetch_by_url(url)["title"],
                director=fetch_by_url(url)["director"]
            )
            for url in s.get("films", [])
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