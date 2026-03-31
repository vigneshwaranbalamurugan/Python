from fastapi import FastAPI

app = FastAPI()

@app.get("/details")
def order_details():
    return {"service": "orders", "message": "Order details"}
@app.get("/list")
def order_list():
    return {"orders": [101, 102, 103]}