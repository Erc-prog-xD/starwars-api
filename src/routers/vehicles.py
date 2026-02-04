from fastapi import APIRouter, Depends


from schemas.types_class import Films, PaginatedVehiclesResponse, People, VehiclesRequest, VehiclesResponse
from services.swapi_services import extract_id_from_url, fetch_data, fetch_data_by_id
from utils.filters import apply_smart_filters, safe_int

router = APIRouter(prefix="/vehicles", tags=["vehicles"])




@router.get("/by-id/{id}")
def get_vehicles_by_id(id: int):
    vehicles_data = fetch_data_by_id("vehicles", id)
    return vehicles_data


@router.get(
    "/list_vehicles_by_filters",
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


@router.get("/stats/overview")
def vehicles_stats_overview():

    vehicles = fetch_data("vehicles")

    classes = {}
    manufacturers = {}

    for v in vehicles:
        cls = v.get("vehicle_class")
        if cls:
            classes[cls] = classes.get(cls, 0) + 1

        man = v.get("manufacturer")
        if man:
            manufacturers[man] = manufacturers.get(man, 0) + 1

    return {
        "total_vehicles": len(vehicles),
        "vehicle_classes": classes,
        "manufacturers": manufacturers
    }


@router.get("/stats/cost")
def vehicles_cost_stats():

    vehicles = fetch_data("vehicles")

    costs = []
    most_expensive = None
    max_cost = 0

    for v in vehicles:
        cost = safe_int(v.get("cost_in_credits", ""))
        if cost is not None:
            costs.append(cost)

            if cost > max_cost:
                max_cost = cost
                most_expensive = {
                    "name": v["name"],
                    "cost_in_credits": cost
                }

    avg_cost = sum(costs) / len(costs) if costs else 0

    return {
        "average_cost": round(avg_cost, 2),
        "most_expensive_vehicle": most_expensive
    }


@router.get("/stats/cargo")
def vehicles_cargo_stats():

    vehicles = fetch_data("vehicles")

    cargos = []
    highest_cargo = None
    max_cargo = 0

    for v in vehicles:
        cargo = safe_int(v.get("cargo_capacity", ""))
        if cargo is not None:
            cargos.append(cargo)

            if cargo > max_cargo:
                max_cargo = cargo
                highest_cargo = {
                    "name": v["name"],
                    "cargo_capacity": cargo
                }

    avg_cargo = sum(cargos) / len(cargos) if cargos else 0

    return {
        "average_cargo_capacity": round(avg_cargo, 2),
        "highest_cargo_vehicle": highest_cargo
    }


@router.get("/stats/speed")
def vehicles_speed_stats():

    vehicles = fetch_data("vehicles")

    speeds = []
    fastest = None
    max_speed = 0

    for v in vehicles:
        speed = safe_int(v.get("max_atmosphering_speed", ""))
        if speed is not None:
            speeds.append(speed)

            if speed > max_speed:
                max_speed = speed
                fastest = {
                    "name": v["name"],
                    "max_atmosphering_speed": speed
                }

    avg_speed = sum(speeds) / len(speeds) if speeds else 0

    return {
        "average_speed": round(avg_speed, 2),
        "fastest_vehicle": fastest
    }


@router.get("/stats/most_appeared_in_movies")
def most_appeared_in_movies():

    vehicles = fetch_data("vehicles")

    result = []

    for v in vehicles:
        result.append({
            "name": v["name"],
            "appearances": len(v.get("films", []))
        })

    result.sort(key=lambda x: x["appearances"], reverse=True)

    return {
        "results": result
    }
