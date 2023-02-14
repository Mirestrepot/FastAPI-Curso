#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel


#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path
app = FastAPI()

#Models
class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name : str
    last_name : str
    age : str
    hair_color : Optional[str] = None
    is_married : Optional[bool] = None
    
    

@app.get('/')
def home():
    return {
        "Hello : World"
    }


@app.post('/person/new')
def create_person(person : Person = Body()):
    return person   

@app.get('/person/detail')
def show_person(
    name : Optional[str] = Query(
        default=None,
        min_length=1,
        max_length= 50,
        title="Person Name",
        description="This is the person name. It's betwwen 1 and 50 characters"),
    age :   Optional[str] =Query(
        default=None,
        min_length=1,
        max_length=20,
        title="Person Age",
        description="This is the person age.It's required")
    ):  return {name:age}

# Validations : Path Paremeter

@app.get("/person/detail/{person_id}")
def show_person(
	title: "Person",
	person_id: int = Path(ge=0)
):
	return {person_id: "It exist!"}

#Validation: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
): 
    results = person.dict()
    results.update((location.dict()))
    return  results