from typing import Optional, Dict, List
from fastapi import FastAPI, Query, Path, Body, File, UploadFile, Depends
from pydantic import BaseModel, Field
from dependencies.pagination import Paginator
app = FastAPI()


# App to print Hello World
@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


# App to pront user name
@app.get("/user/{user_name}", response_model=Dict[str, str])
async def read_user_name(user_name: str) -> Dict[str, str]:
    ''' Returns the input sting as the designated username'''
    return {"Name": user_name}

users = [{"name": "dinesh", "age": 27},
         {"name": "dipesh", "age": 30},
         {"name": "dewaki", "age": 50},
         ]


# Example of Query Parameters
@app.get("/users/", response_model=Dict[str, str])
async def get_user_details(user_name: Optional[str] = None, page: int = 10):
    if not user_name:
        return users[0:page]


# Model for Items
class Item(BaseModel):
    name: str = Field(..., description="Name of the Items", max_length=50)
    description: Optional[str] = Field(None, description="Product Desc")
    price: float = Field(..., description="Price of Item per unit", gt=0)
    tax: Optional[float] = Field(None, description="Taxation Rate", lt=50)
    tags: List[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


# POST operation for items
@app.post("/items/", response_model=Item)
async def create_item(item: Item, weight: int = Body(...), pages: Optional[Paginator] = Depends()):  # noqa
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}", response_model=Item)
async def create_items(*, item_id: int = Path(...,
                                              description="Item Identification",  # noqa
                                              gt=0,
                                              lt=1000),
                       item: Item = Body(..., embed=True),
                       q: Optional[List[str]] = Query(...,
                                                      min_length=3,
                                                      title="Query Parameter",
                                                      description="Test Description",  # noqa
                                                      alias="query",
                                                      deprecated=True,
                                                      regex="^fixedquery$",
                                                      max_length=50)):
    return {"item_id": item_id, **item.dict()}


# Example of Query Parameters
@app.get("/files/", tags=["files"])
async def get_files(file_name: str):
    return file_name


# Example of Query Parameters
@app.post("/files/", tags=["files"])
async def post_files(files: UploadFile = File(...)):
    return {"message": "File stored",
            "content-type": files.content_type,
            "file": files.file,
            "file_name": files.filename}


# POST operation for items
@app.get("/pages/")
async def get_pages(pages: Paginator = Depends()):
    return Paginator.get_doc()
