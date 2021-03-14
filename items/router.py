from fastapi import APIRouter, Depends, HTTPException

from dependencies.pagination import page_info

item = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(page_info)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@item.get(
    "/",
    tags=["read"],
)
async def read_items():
    return fake_items_db


@item.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@item.put(
    "/{item_id}",
    tags=["update"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
