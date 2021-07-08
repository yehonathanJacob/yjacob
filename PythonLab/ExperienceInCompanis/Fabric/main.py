import argparse
from typing import List
from enum import Enum

from starlette.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
import uvicorn

DATA = [[-1]*10]*10
MAP_NAME_TO_DATA = {}

def get_product_index(name):
    if name not in MAP_NAME_TO_DATA:
        insert_product_to_data(name)

    return MAP_NAME_TO_DATA[name]


def insert_product_to_data(name):
    selected_i, selected_j, selected_row = None, None, None
    for i, row in enumerate(DATA):
        find = False
        for j, value in enumerate(row):
            if value == -1:
                selected_i, selected_j = i, j
                find = True
                break

        if find:
            break

    if selected_i is None:
        raise EOFError()

    DATA[selected_i][selected_j] = 0
    MAP_NAME_TO_DATA[name] = (selected_i, selected_j)

def valid_product(name):
    if name not in MAP_NAME_TO_DATA:
        return False

    i, j = MAP_NAME_TO_DATA[name]
    return DATA[i][j] > 0

app = FastAPI()

class RobotActions(Enum):
    PUT_TO_STOCK = 'put_to_stock'
    PICK_FROM_STOCK = 'pick_from_stock'

class Tasks:
    TASK_DICT = {}
    LAST_TASK = 0
    LAST_ID = 0

    @classmethod
    def insert_task(cls, action: RobotActions, product_name: str, location: List[int]):
        id = cls._get_id()
        task = {'id': id, 'action': action.value, 'product': product_name, 'location': location}
        cls.TASK_DICT[id] = task

    @classmethod
    def _get_id(cls):
        id = cls.LAST_ID
        cls.LAST_ID += 1
        return id

    @classmethod
    def is_valid_task(cls):
        return cls.LAST_TASK < cls.LAST_ID

    @classmethod
    def get_task(cls):
        if cls.is_valid_task():
            task = cls.TASK_DICT[cls.LAST_TASK]
            cls.LAST_TASK += 1
            return task
        raise EOFError('All task are called.')

    @classmethod
    def complete_task(cls, id:int):
        task = cls.TASK_DICT[id]
        action = RobotActions(task['action'])
        if action == RobotActions.PUT_TO_STOCK:
            i, j = task['location']
            DATA[i][j] += 1
        elif action == RobotActions.PICK_FROM_STOCK:
            i, j = task['location']
            DATA[i][j] -= 1
            if DATA[i][j] == 0:
                DATA[i][j] = -1
                MAP_NAME_TO_DATA.pop(task['product'], None)

        cls.TASK_DICT.pop(id, None)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs/")

@app.post("/order")
def order(products: List[str]):
    if not len(products) > 0:
        raise HTTPException(status_code=400, detail=f"You must order at least one product")

    for product_name in products:
        if not valid_product(product_name):
            raise HTTPException(status_code=400, detail=f"Could not order {product_name} because it is out of stock")

    for product_name in products:
        location = get_product_index(product_name)
        Tasks.insert_task(RobotActions.PICK_FROM_STOCK, product_name, location)

@app.post("/supply")
def supply(products: List[str]):
    if not len(products) > 0:
        raise HTTPException(status_code=400, detail=f"You must order at least one product")

    for product_name in products:
        location = get_product_index(product_name)
        Tasks.insert_task(RobotActions.PUT_TO_STOCK, product_name, location)

@app.post("/tasks/{id}/complete")
def complete(id: int):
    if not id in Tasks.TASK_DICT:
        raise HTTPException(status_code=400, detail=f"Task id: {id} not exist")

    Tasks.complete_task(id)

@app.get("/next-tasks")
def next_tasks():
    if not Tasks.is_valid_task():
        raise HTTPException(status_code=400, detail=f"There is no valid task")

    tasks = []
    while Tasks.is_valid_task():
        tasks.append(Tasks.get_task())

    return tasks

@app.get("/stock")
def stock():
    data = []
    for product_name, (i, j) in MAP_NAME_TO_DATA.items():
        amount = DATA[i][j]
        data.append([product_name, [i, j], amount])

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default=8000, type=int)
    parser.add_argument('--mode', default="DEBUG")
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)
