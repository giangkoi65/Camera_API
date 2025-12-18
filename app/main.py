from fastapi import FastAPI

app = FastAPI()
items = []


@app.get("/")
def root():
    return {"Hello": "World"}


# @app.post("/items")
# def create_item(name: str):
#     items.append(name)
#     return {"item": name}
