# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, menu, orders, profile, favorites, allergens, ai

app = FastAPI(
    title="SafePlate API 🍽️",
    description="Backend",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(menu.router, prefix="/menu")
app.include_router(allergens.router, prefix="/allergens")
app.include_router(orders.router, prefix="/orders")
app.include_router(profile.router, prefix="/profile")
app.include_router(favorites.router, prefix="/favorites")
app.include_router(ai.router, prefix="/ai")  

@app.get("/")
def root():
    return {"message": "SafePlate FastAPI backend is running ✅"}

@app.get("/routes")
def list_routes():
    return [{"path": route.path, "methods": list(route.methods)} for route in app.routes]