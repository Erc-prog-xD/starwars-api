from fastapi import APIRouter, Depends


from schemas.types_class import Films, PaginatedVehiclesResponse, People, VehiclesRequest, VehiclesResponse
from services.swapi_services import extract_id_from_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters

router = APIRouter(prefix="/vehicles", tags=["vehicles"])




@router.get("/by-id/{id}")
def get_vehicles_by_id(id: int):
    vehicles_data = fetch_data_by_id("vehicles", id)
    return vehicles_data


@router.get(
    "/list_by_filters",
    response_model=PaginatedVehiclesResponse
)
def list_vehicles_by_filters(request: VehiclesRequest = Depends()):

    vehicles_data = fetch_data("vehicles")
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
    if request.vehicle_class:
        filters["vehicle_class"] = request.vehicle_class

    result = (
        vehicles_data if not filters
        else apply_smart_filters(vehicles_data, filters)
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

    response: list[VehiclesResponse] = []

    for v in paginated:

        pilots = [
            People(name=people_map[url]["name"])
            for url in v.get("pilots", [])
            if url in people_map
        ]

        films = [
            Films(
                title=films_map[url]["title"],
                director=films_map[url]["director"]
            )
            for url in v.get("films", [])
            if url in films_map
        ]

        response.append(
            VehiclesResponse(
                name=v["name"],
                model=v["model"],
                manufacturer=v["manufacturer"],
                cost_in_credits=v["cost_in_credits"],
                length=v["length"],
                max_atmosphering_speed=v["max_atmosphering_speed"],
                crew=v["crew"],
                passengers=v["passengers"],
                cargo_capacity=v["cargo_capacity"],
                consumables=v["consumables"],
                vehicle_class=v["vehicle_class"],
                pilots=pilots,
                films=films,
                url_id=v["url"]
            )
        )

    return PaginatedVehiclesResponse(
        page=request.page,
        page_size=request.page_size,
        total=total,
        results=response
    )
