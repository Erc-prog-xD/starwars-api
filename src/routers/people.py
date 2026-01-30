# routers/people.py
from fastapi import APIRouter, Depends, Query
from schemas.types_class import Films, GenderCountResponse, PeopleRequest, PeopleResponse, StatisticHeightResponse, StatisticMassResponse, TypeGender
from services.swapi_services import fetch_data
from utils.filters import apply_exact_filters, apply_smart_filters, filter_no_gender

router = APIRouter(prefix="/people", tags=["people"])

@router.get(
    "/gender_count",
    response_model=GenderCountResponse,
    response_model_exclude_unset=True
)
def gender_count():
    data = fetch_data("people")

    masc_filter = {"gender": "male"}
    fem_filter = {"gender": "female"}

    result_masc = apply_exact_filters(data, masc_filter)
    result_fem = apply_exact_filters(data, fem_filter)

    count_masc = len(result_masc)
    count_fem = len(result_fem)
    count_total = len(data)

    response = GenderCountResponse(
        male_count=count_masc,
        female_count=count_fem,
        total=count_total,
        no_gender_specified= count_total - (count_fem + count_masc)
    )

    return response


@router.get(
    "/statistics_height_people",
    response_model=StatisticHeightResponse,
    response_model_exclude_unset=True
)
def statistics_height_people(gender: TypeGender = Query(None, description="type gender")):
    data = fetch_data("people")

    if gender == TypeGender.others:
        result = filter_no_gender(data)
    elif gender:
        result = apply_exact_filters(data, {"gender": gender.value})
    else:
        result = data
    
    heights = []
    for person in result:
        if person["height"].isdigit():
            heights.append(int(person["height"]))

    if not heights:
        avg_height = min_height = max_height = 0
        count_total = 0
    else:
        avg_height = sum(heights) / len(heights)
        min_height = min(heights)
        max_height = max(heights)
        count_total = len(heights)

    response = StatisticHeightResponse(
        gender = gender,
        count_total_people= count_total,
        avgHeight= avg_height,
        minHeight= min_height,
        maxHeight= max_height
    )
    return response


@router.get(
    "/statistics_mass_people",
    response_model=StatisticMassResponse,
    response_model_exclude_unset=True
)
def statistics_mass_people(gender: TypeGender = Query(None, description="type gender")):
    data = fetch_data("people")

    if gender == TypeGender.others:
        result = filter_no_gender(data)
    elif gender:
        result = apply_exact_filters(data, {"gender": gender.value})
    else:
        result = data

    masses = []

    for person in result:
        if person["mass"].isdigit():
            masses.append(int(person["mass"]))

    if not masses:
        avg_mass = min_mass = max_mass = 0
        count_total = 0
    else:
        avg_mass = sum(masses) / len(masses)
        min_mass = min(masses)
        max_mass = max(masses)
        count_total = len(masses)

    response = StatisticMassResponse(
        gender=gender,
        count_total_people=count_total,
        avgMass=avg_mass,
        minMass=min_mass,
        maxMass=max_mass
    )

    return response

@router.get(
    "/list_people_by_filters",
    response_model=list[PeopleResponse],
    response_model_exclude_unset=True
)
def list_people_by_filters(
    request: PeopleRequest = Depends()
):
    people_data = fetch_data("people")
    films_data = fetch_data("films")

    films_map = {
        film["url"]: film["title"]
        for film in films_data
    }

    filters = {}

    if request.name:
        filters["name"] = request.name
    if request.gender:
        filters["gender"] = request.gender.value
    if request.hair_color:
        filters["hair_color"] = request.hair_color
    if request.eye_color:
        filters["eye_color"] = request.eye_color
    if request.birth_year:
        filters["birth_year"] = request.birth_year

    if not filters:
        result = people_data
    else:
        result = apply_smart_filters(people_data, filters)

    response = []

    for p in result:
        films = [
            Films(title=films_map[url])
            for url in p.get("films", [])
            if url in films_map
        ]

        response.append(
            PeopleResponse(
                name=p["name"],
                gender=p["gender"],
                hair_color=p["hair_color"],
                eye_color=p["eye_color"],
                skin_color=p["skin_color"],
                birth_year=p["birth_year"],
                films=films
            )
        )

    return response