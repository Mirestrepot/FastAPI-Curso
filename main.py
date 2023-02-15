#Python
from typing import Optional
from enum import Enum


#Pydantic
from pydantic import (
    BaseModel,
    Field,
    EmailStr)

#FastAPI
from fastapi import (
    FastAPI,UploadFile,status,HTTPException,
    Body,Query,Path,Form,
    Header,Cookie,File,)


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

class BasePerson(BaseModel):
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
    
class Person(BasePerson):
    password: str = Field(..., min_length=8)
    
    class Config:
        
        schema_extra = {
            "example": {

                "first_name": "Miguel",
                "last_name": "Restrepo",
                "age": 23,
                "hair_color": "brown",
                "is_married": False,
                "password": "contraseña123"
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

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="Miguel0123"
    )
    message: str = Field(default="Login Succesfully!")
        
    
#Examples
persons = [1,2,3,4,5]
user_list = [
    Person(
        first_name= "Miguel",
        last_name= "Restrepo",
        age= 23,
        hair_color= "brown",
        is_married= False,
        password= "contraseña123"),
    Person(
        first_name= "Isa",
        last_name= "Restrepo",
        age= 27,
        hair_color= "brown",
        is_married= True,
        password= "password123")
    
]


    

@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home page"
    )
async def home():
    return {
        "Hello : World"
    }

#Request and Response Body
@app.post(
    path='/person/new',
    response_model=BasePerson,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="create a new person"
    )
async def create_person(person : Person = Body()):
    """create_person
    Description: create a new person
    Parameters: person (Person)

    Returns: person
    """
    return person   


#Validation: Query Parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary= "Show a person detail (name,age)",
    deprecated=True
    )
async def show_person(
    name : Optional[str] = Query(
        default=None,
        min_length=1,
        max_length= 50,
        title="Person Name",
        description="This is the person name. It's betwwen 1 and 50 characters",
        example="Rocio"
        ),
    age :   Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=20,
        title="Person Age",
        description="This is the person age.It's required",
        example=25
        )
    ):
    """Show person
    Parameters: name,age
    Description: Show person and age
    Returns:
        name,age
    """
    return {name:age}

# Validations : Path Paremeter

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Show person"
    )
async def show_person(
	person_id: int = Path(
        ...,
        ge=0,
        example=123
    )
):  
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist"
        )
    """show_person
    Parameters: person_id
    Description: Show id of person
    Returns:ID person  
    """
    return {person_id: "It exist!"}


#Validation: Request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"])
async def update_person(
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

#Forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username=username)
    
#Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Forms"]
)
async def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1     
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
        message: str = Form(
        ...,
        min_length=20 
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["Files"]
)
async def post_image(
    image: UploadFile = File(...)
):
    return{
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2),
    }
