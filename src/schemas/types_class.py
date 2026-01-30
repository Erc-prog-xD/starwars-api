
from enum import Enum
from typing import Optional

from pydantic import BaseModel

class Types(str, Enum):
    people = "people"
    planets = "planets"
    films = "films"
    starships = "starships"

class TypeGender(str, Enum):
    male = "male"
    female = "female"
    others = "others"


class Films(BaseModel):
    title: str


class PeopleRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[TypeGender] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    skin_color: Optional[str] = None
    birth_year: Optional[str] = None

class PeopleResponse(BaseModel):
    name: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    films: list[Films]


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
