
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # ADD THIS

from app.database import Base, engine, SessionLocal
from app import models, schemas, crud
from app.routes.ai import router as ai_router
from app.routes import performance
from app.routes import auth

# Create FastAPI app FIRST
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app"  # add deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create DB tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ROOT
@app.get("/")
def home():
    return {
        "message": "LearnScape API Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# USER CRUD
@app.post("/users")
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)


@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    return crud.get_users(db)


@app.get("/users/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return crud.get_user(db, user_id)


@app.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    return crud.delete_user(db, user_id)


# AI ROUTES
app.include_router(
    ai_router,
    prefix="/ai"
)

# PERFORMANCE ROUTES
app.include_router(
    performance.router
)

# VERCEL HANDLER
handler = Mangum(app)
