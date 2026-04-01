from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio

from simulator import simulator
from process import ProcessSensorData

app = FastAPI()

processor = ProcessSensorData()

@app.get("/")
async def home():
    return FileResponse("index.html")

@app.get("/style.css")
async def style():
    return FileResponse("style.css")

@app.get("/script.js")
async def script():
    return FileResponse("script.js")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for data in simulator():
            processed = processor.processdata(data)
            await websocket.send_json(processed)
    except Exception as e:
        print("WebSocket disconnected:", e)