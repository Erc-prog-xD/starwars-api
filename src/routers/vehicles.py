from fastapi import APIRouter, Depends


from schemas.types_class import Films, PaginatedVehiclesResponse, People, VehiclesRequest, VehiclesResponse
from services.swapi_services import fetch_data, fetch_by_url, fetch_data_by_id
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

    total = len(result)

    start = (request.page - 1) * request.page_size
    end = start + request.page_size
    paginated = result[start:end]

    response = []

    for v in paginated:

        pilots = [
            People(name=fetch_by_url(url)["name"])
            for url in v.get("pilots", [])
        ]

        films = [
            Films(
                title=fetch_by_url(url)["title"],
                director=fetch_by_url(url)["director"]
            )
            for url in v.get("films", [])
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
                films=films
            )
        )

    return PaginatedVehiclesResponse(
        page=request.page,
        page_size=request.page_size,
        total=total,
        results=response
    )
