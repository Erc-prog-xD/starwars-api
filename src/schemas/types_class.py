
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class Types(str, Enum):
    people = "people"
    planets = "planets"
    films = "films"
    starships = "starships"
    species = "species"
    vehicles = "vehicles"


class TypeGender(str, Enum):
    male = "male"
    female = "female"
    others = "others"

class People(BaseModel):
    name: str

class Species(BaseModel):
    name: str
    classification: str

class Films(BaseModel):
    title: str
    director: str

class Vehicles(BaseModel):
    name: str
    model: str

class Starships(BaseModel):
    name: str
    model: str
    pilots: list[str]

class Planets(BaseModel):
    name: str
    population: int | str


#-- PEOPLE

class PeopleRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[TypeGender] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    skin_color: Optional[str] = None
    birth_year: Optional[str] = None

    order_by: Optional[str] = "url"
    order_dir: Optional[str] = "asc"

    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=50)

class PeopleResponse(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: list[Films]
    species: list[Species]
    vehicles: list[Vehicles]
    starships: list[Starships]
    url_id: str

class PaginatedPeopleResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[PeopleResponse]


class GenderCountResponse(BaseModel):
    male_count: int
    female_count: int
    total: int
    no_gender_specified: int

class StatisticHeightResponse(BaseModel):
    gender: Optional[TypeGender]
    count_total_people: int
    avgHeight: float
    minHeight: float
    maxHeight: float

class StatisticMassResponse(BaseModel):
    gender: Optional[TypeGender]
    count_total_people: int
    avgMass: float
    minMass: float
    maxMass: float



#-- PLANETS



class PlanetResponse(BaseModel):
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    population: str
    surface_water: str
    residents: list[People]
    films: list[Films]
    url_id: str

class PlanetRequest(BaseModel):
    name: Optional[str] = None
    climate: Optional[str] = None
    terrain: Optional[str] = None
    min_population: Optional[int] = None

    order_by: Optional[str] = "url"
    order_dir: Optional[str] = "asc"

    page: int = 1
    page_size: int = 10

class PaginatedPlanetsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[PlanetResponse]

class TopPlanetsByPopulation(BaseModel):
    with_population: list[Planets]
    without_population: list[Planets]

class Residents(BaseModel):
    name: str
    residents_count: int

class TopPlanetsByResidents(BaseModel):
    result: list[Residents]

class PopulationStatisticsResponse(BaseModel):
    total_planets: int
    inhabited: int
    not_inhabited: int
    avg_population: float
    max_population: int
    min_population: int



#-- FILMS

class FilmsResponse(BaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str
    characters: list[People]
    planets: list[Planets]
    starships: list[Starships]
    vehicles: list[Vehicles]
    species: list[Species]
    url_id: str

class FilmWithCounts(BaseModel):
    title: str
    characters_count: int
    planets_count: int
    starships_count: int
    vehicles_count: int
    species_count: int

class PaginatedFilmsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[FilmsResponse]

class FilmsRequest(BaseModel):
    title: Optional[str] = None
    episode_id: Optional[int] = None
    director: Optional[str] = None
    producer: Optional[str] = None
    release_date: Optional[date] = None

    order_by: Optional[str] = "url"
    order_dir: Optional[str] = "asc"

    page: int = 1
    page_size: int = 10

class FilmsWithCountsResponse(BaseModel):
    results: list[FilmWithCounts]

class moviesCharacterAppeared(BaseModel):
    name: str
    movie: list[Films]

class moviesCharacterAppearedResponse(BaseModel):
    results: list[moviesCharacterAppeared]

#- STARSHIPS

class StarshipsResponse(BaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str
    starship_class: str
    pilots: list[People]
    films: list[Films]
    url_id: str

class StarshipsRequest(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    starship_class: Optional[str] = None

    order_by: Optional[str] = "url"
    order_dir: Optional[str] = "asc"

    page: int = 1
    page_size: int = 10
    
class PaginatedStarshipsResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[StarshipsResponse]



# Species

class SpeciesResponse(BaseModel):
    name: str
    classification: str
    designation: str
    average_height: str
    skin_colors: str
    hair_colors: str
    eye_colors: str
    average_lifespan: str
    homeworld: Optional[str]
    language: str
    people: list[People]
    films: list[Films]
    url_id: str

class SpeciesRequest(BaseModel):
    name: Optional[str] = None
    classification: Optional[str] = None
    designation: Optional[str] = None
    language: Optional[str] = None

    order_by: Optional[str] = "url"
    order_dir: Optional[str] = "asc"

    page: int = 1
    page_size: int = 10

class PaginatedSpeciesResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[SpeciesResponse]



# VEHICLES

class VehiclesResponse(BaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    vehicle_class: str
    pilots: list[People]
    films: list[Films]
    url_id: str


class VehiclesRequest(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    vehicle_class: Optional[str] = None

    order_by: Optional[str] = "url"
    order_dir: Optional[str] = "asc"

    page: int = 1
    page_size: int = 10

class PaginatedVehiclesResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[VehiclesResponse]

