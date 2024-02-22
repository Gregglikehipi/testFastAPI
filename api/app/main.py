from fastapi import FastAPI
from app.Parser import get_detail, get_quantity, get_history_price
from pydantic import BaseModel
from typing import Dict, Optional, List
from app.DBHelper import DBHelper


class Item(BaseModel):
    nm_id: int
    name: str
    name: str
    brand: str
    brand_id: int
    site_brand_id: int
    supplier_id: int
    sale: int
    price: int
    sale_price: int
    rating: int
    feedbacks: int
    colors: Optional[str]
    qnt: int
    subjectId: int


class Prices(BaseModel):
    price: List[Dict[str, int]]


class ListItems(BaseModel):
    list: List[int]


app = FastAPI()
helper = DBHelper()


@app.post("/add/{item_id}")
def add_item(item_id: int):
    req = get_detail(item_id)
    qnt_req = get_quantity(item_id)
    req['qnt'] = qnt_req[0]['qnt']
    print(req)
    helper.add_item(req)
    item = Item(**req)
    req_history = get_history_price(item_id)
    helper.add_price_history(req_history)
    return item


@app.get("/get/{item_id}")
def get_item(item_id: int):
    item = Item(**helper.get_item(item_id))
    return item


@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    helper.delete_item(item_id)
    return {"Hello": "World"}


@app.get("/get_all")
def get_all_item():
    ans = helper.get_all_item()
    ans = {"list": ans}
    items = ListItems(**ans)
    return items


@app.get("/countAll")
def get_all_item():
    ans = helper.qnt_all_items()
    print(ans)
    return {"ans": ans}


@app.get("/countGroup/{subject_id}")
def get_all_item(subject_id: int):
    ans = helper.qnt_group_items(subject_id)
    return {"ans": ans}


@app.get("/historyPrice/{item_id}")
def get_all_item(item_id: int):
    ans = helper.get_price_history(item_id)
    ans = {"price": ans}
    print(ans)
    price = Prices(**ans)
    return price


@app.get("/comparePrice/{item_id}")
def get_all_item(item_id: int):
    ans = helper.get_item(item_id)
    subject_id = ans['subjectId']
    price = ans['price']
    avgPrice = helper.get_avg_price(subject_id)
    return {"price": price, "avgPrice": avgPrice}
