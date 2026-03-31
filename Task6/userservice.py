from fastapi import FastAPI

app = FastAPI()

@app.get("/profile")
def get_profile():
    return {"service": "users", "message": "User profile data"}

@app.get("/list")
def get_users():
    return {"users": ["Vignesh", "Shriran", "Vijay"]}