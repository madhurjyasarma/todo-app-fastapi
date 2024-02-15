from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    is_done: Optional[bool] = False


# In-memory database
db = []
db_id_counter = 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/", response_model=Item)
def create_item(item: Item):
    global db_id_counter
    new_item = {"id": db_id_counter, **item.dict()}
    db.append(new_item)
    db_id_counter += 1
    return new_item


@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return db[skip: skip + limit]


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = next((i for i in db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    index = next((i for i, d in enumerate(db) if d["id"] == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db[index] = {"id": item_id, **item.dict()}
    return db[index]


@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    item = next((i for i in db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.remove(item)
    return item
