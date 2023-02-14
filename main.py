#Python
from typing import Optional
from enum import Enum


#Pydantic
from pydantic import BaseModel
from pydantic import Field


#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path

app = FastAPI()

#Models
class HairColor(str, Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
    
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50)
    
    state: str = Field(
        ...,
        min_length=1,
        max_length=50)
    
    country: str = Field(
        ...,
        min_length=1,
        max_length=50)
    
    class Config:
        schema_extra = {
            "example": {

                "city": "La Estrella",
                "state": "Antioquia",
                "country": "Colombia",
            }
        }

class Person(BaseModel):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50)
    
    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50)
    
    age : int = Field(
        ...,
        gt=0,
        le=115)
    hair_color : Optional[HairColor] = Field(default=None) 
    
    is_married : Optional[bool]  = Field(default=None)
    class Config:

        schema_extra = {
            "example": {

                "first_name": "Miguel",
                "last_name": "Restrepo",
                "age": 23,
                "hair_color": "brown",
                "is_married": False
            }
        }

        #     "example 2": {
        #         "first_name": "Rodrigo",
        #         "last_name": "Lopez",
        #         "age": 30,
        #         "hair_color": "black",
        #         "is_married": False
        #     }
        # }
        
        
    



    

@app.get('/')
def home():
    return {
        "Hello : World"
    }


@app.post('/person/new')
def create_person(person : Person = Body()):
    return person   


#Validation: Query Parameters
@app.get('/person/detail')
def show_person(
    name : Optional[str] = Query(
        default=None,
        min_length=1,
        max_length= 50,
        title="Person Name",
        description="This is the person name. It's betwwen 1 and 50 characters",
        example="Rocio"
        ),
    age :   Optional[str] =Query(
        default=None,
        min_length=1,
        max_length=20,
        title="Person Age",
        description="This is the person age.It's required",
        example=25
        )

    ):  return {name:age}

# Validations : Path Paremeter

@app.get("/person/detail/{person_id}")
def show_person(
	person_id: int = Path(
    ...,
    ge=0,
    example=123
    )
):
	return {person_id: "It exist!"}

#Validation: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
): 
    results = person.dict()
    results.update((location.dict()))
    return  results
