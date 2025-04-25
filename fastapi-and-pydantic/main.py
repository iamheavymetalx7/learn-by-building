from fastapi import FastAPI, HTTPException
from pydantic_demo import BaseModel

items =[]
app = FastAPI()


class Item(BaseModel):
    text: str = None
    is_done: bool = False
    
    
@app.get("/") 
def root():
    return {"Hello":"Nitish"}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get('/items', response_model= list[Item])
def list_items(limit : int = 10):
    return items[:limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail="Item  {item_id} not found")   
    