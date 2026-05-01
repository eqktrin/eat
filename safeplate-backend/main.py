from database import engine, Base
import models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import auth, menu, orders, profile, favorites, allergens, ai, images, seo, external_api, weather
import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SafePlate API 🍽️",
    description="Backend",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
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
app.include_router(images.router)
app.include_router(seo.router)
app.include_router(external_api.router)
app.include_router(weather.router)

@app.get("/")
def root():
    return {"message": "SafePlate FastAPI backend is running"}

@app.get("/routes")
def list_routes():
    routes = []
    for route in app.routes:
        methods = list(route.methods) if hasattr(route, "methods") else []
        routes.append({"path": route.path, "methods": methods})
    return routes

# 👇 ДОБАВЬ ЭТО
@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")