from fastapi import APIRouter, Depends, Query

from schemas.types_class import Films, PaginatedSpeciesResponse, People, SpeciesRequest, SpeciesResponse
from services.swapi_services import extract_id_from_url, fetch_by_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters




router = APIRouter(prefix="/species", tags=["species"])

@router.get("/by-id/{id}")
def get_species_by_id(id: int):
    species_data = fetch_data_by_id("species", id)
    return species_data




@router.get(
    "/species/list_by_filters",
    response_model=PaginatedSpeciesResponse
)
def list_species_by_filters(request: SpeciesRequest = Depends()):

    species_data = fetch_data("species")

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

        people = [
            People(name=fetch_by_url(url)["name"])
            for url in s.get("people", [])
        ]

        films = [
            Films(
                title=fetch_by_url(url)["title"],
                director=fetch_by_url(url)["director"]
            )
            for url in s.get("films", [])
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
                homeworld=s["homeworld"],
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
