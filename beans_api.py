#!/bin/python3
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response
from enum import Enum
from pydantic import BaseModel

CUR_ID = 0

def generate_beans_id():
    global CUR_ID
    CUR_ID += 1
    return CUR_ID


class BeansType(str, Enum):
    arabica = "arabica"
    robusta = "robusta"
    liberca = "liberca"
    excelsa = "excelsa"

class BeansRegion(str, Enum):
    colombia = "colombia"
    brazil = "brazil"
    sumata = "sumata"
    kenya = "kenya"

class BeansRoast(str, Enum):
    light = "light"
    medium = "medium"
    dark = "dark"

class BeansItemInput(BaseModel):
    type: BeansType
    region: BeansRegion
    roast: BeansRoast
    quantity: int
    limited: bool

class BeansItem(BaseModel):
    id: int
    type: BeansType
    region: BeansRegion
    roast: BeansRoast
    quantity: int
    limited: bool = False
    deleted: bool = False


beans_inventory = []

app = FastAPI()

@app.post("/beans/", response_model=BeansItem, status_code=201)
def post_beans_item(beans_in_item: BeansItemInput):
    beans_id = generate_beans_id() 
    beans_item = {"id": beans_id, "deleted": False, **beans_in_item.dict()}
    beans_inventory.append(BeansItem(**beans_item))
    return BeansItem(**beans_item)

@app.get("/beans/all", response_model=List[BeansItem], status_code=200)
def get_all_beans():
    result = [ item for item in beans_inventory if not item.deleted ]
    return result

@app.get("/beans/{beans_id}", response_model=BeansItem, status_code=200)
def get_beans(beans_id: int):
    result = [ item for item in beans_inventory if not item.deleted and item.id == beans_id ]

    if not result:
        raise HTTPException(status_code=404, detail='Beans not found')

    return result[0]

@app.put("/beans/{beans_id}", response_model=BeansItem, status_code=200)
def put_beans_item(beans_id: int, beans_in_item: BeansItemInput):
    result = None
    for i, item in enumerate(beans_inventory):
        if item.id == beans_id and not item.deleted:
            beans_item = {"id": beans_id, "deleted": False, **beans_in_item.dict()}
            beans_inventory[i] = BeansItem(**beans_item)
            result = beans_inventory[i]

    if not result:
        raise HTTPException(status_code=404, detail='Beans cannot be updated')

    return result

@app.delete("/beans/{beans_id}", status_code=204)
def delete_beans_item(beans_id: int):
    item = [ item for item in beans_inventory if item.id == beans_id ]

    if not item:
        raise HTTPException(status_code=404, detail='Beans cannot be deleted')

    for i, item in enumerate(beans_inventory):
        if item.id == beans_id:
            item.deleted = True

    # avoid "too much data" error and return a Response instead
    return Response(status_code=204)
