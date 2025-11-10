from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_id = item.item_id
    needy = item.needy
    skip = item.skip
    limit = item.limit
    item.name = item.name
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    # FastAPI 能识别与路径参数匹配的函数参数，还能识别从请求体中获取的类型为 Pydantic 模型的函数参数。
    return {"item_id": item_id, **item.dict()}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


