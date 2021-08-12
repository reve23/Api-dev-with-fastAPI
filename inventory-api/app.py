from fastapi import FastAPI,Path
from typing import Optional
import datetime 
from pydantic import BaseModel

app = FastAPI()

inventory = {}
@app.get("/get-all")
def get_item():
    return inventory

@app.get("/get-item/{item_id}")
def get_item(item_id:int):
    return inventory[item_id]

@app.get("/get-item-by-name/{item_id}")
def get_item(*,item_id:int,name:Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not Found"}

class Item(BaseModel):
    name: str
    price: float
    expires: Optional[str] = None

@app.post("/add-item/{item_id}")
def add_item(item_id:int,item:Item):
    if item_id in inventory:
        return {"Error":"Item Id already exists"}
    inventory[item_id] = {"name":item.name,"price":item.price,"expires":item.expires}
    return inventory[item_id]
    
#update a item
class UpdateItem(BaseModel):
    name : Optional[str] = None
    price : Optional[str] = None
    brand : Optional[str] = None

@app.put("/update-item/{item_id}")
def update_item(item_id:int,item:UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item Id doesnot exist"}
    if item.name != None:
        inventory[item_id]["name"] = item.name
    if item.price != None:
        inventory[item_id]["price"] = item.price
    if item.brand != None:
        inventory[item_id]["brand"] = item.brand
    return inventory[item_id]