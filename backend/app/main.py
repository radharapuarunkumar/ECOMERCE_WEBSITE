from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, SessionLocal
from . import models
from .security import hash_password
from .routers import auth, products, orders, admin


# ==================================================
# CORS CONFIGURATION
# ==================================================

DEFAULT_ORIGINS = [
    "https://ecomerce-website-wheat.vercel.app",
    "https://ecomerce-website-git-main-radharapuarunkumar-projects.vercel.app",
    "http://localhost:3000",
]

configured_origins = [
    origin.strip().rstrip("/")
    for origin in settings.frontend_url.split(",")
    if origin.strip()
]

origins = list(dict.fromkeys(DEFAULT_ORIGINS + configured_origins))


# ==================================================
# DEMO PRODUCTS
# ==================================================

DEMO = [
    {
        "name": "AeroBeat Pro Headphones",
        "category": "Audio",
        "price": 3499,
        "old_price": 4999,
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
        "description": "Immersive sound, all-day comfort and rich bass.",
        "stock": 18,
        "badge": "BESTSELLER",
    },
    {
        "name": "Nova X Smartwatch",
        "category": "Wearables",
        "price": 4299,
        "old_price": 5999,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
        "description": "Your health, activity and notifications at a glance.",
        "stock": 12,
        "badge": "TRENDING",
    },
    {
        "name": "UrbanFlex Sneakers",
        "category": "Fashion",
        "price": 2899,
        "old_price": 3999,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
        "description": "Everyday comfort meets street-ready style.",
        "stock": 25,
        "badge": "NEW",
    },
    {
        "name": "PixelGlow Desk Lamp",
        "category": "Home",
        "price": 1599,
        "old_price": 2199,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80",
        "description": "Minimal lighting for your most focused moments.",
        "stock": 31,
        "badge": "HOT DEAL",
    },
    {
        "name": "TerraPack Backpack",
        "category": "Accessories",
        "price": 1999,
        "old_price": 2799,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
        "description": "A durable daily pack with a padded laptop sleeve.",
        "stock": 16,
        "badge": "POPULAR",
    },
    {
        "name": "VividCam Mini",
        "category": "Electronics",
        "price": 7499,
        "old_price": 8999,
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80",
        "description": "Capture more from your trips and everyday life.",
        "stock": 8,
        "badge": "PREMIUM",
    },
]


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

def initialize():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Create the admin account if it doesn't exist.
        email = settings.admin_email.lower().strip()

        admin_user = (
            db.query(models.User)
            .filter(models.User.email == email)
            .first()
        )

        if not admin_user:
            admin_user = models.User(
                name="NovaCart Admin",
                email=email,
                password_hash=hash_password(settings.admin_password),
                role="admin",
            )

            db.add(admin_user)
            db.commit()

        # Add demo products when the products table is empty.
        if (
            settings.seed_demo_products
            and db.query(models.Product).count() == 0
        ):
            db.add_all(
                [models.Product(**product) for product in DEMO]
            )
            db.commit()

    finally:
        db.close()


# ==================================================
# APPLICATION LIFESPAN
# ==================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="NovaCart API",
    version="1.0.0",
    description="NovaCart e-commerce API with authentication and database support",
    lifespan=lifespan,
)


# ==================================================
# MIDDLEWARE
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# API ROUTERS
# ==================================================

app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


# ==================================================
# HEALTH CHECKS
# ==================================================

@app.get("/")
def root():
    return {
        "name": "NovaCart API",
        "status": "ok",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "api": "ok",
        "database": "connected",
    }