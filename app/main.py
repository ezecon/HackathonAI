
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from mangum import Mangum

# Local imports
from .database import SessionLocal
from . import schemas, crud

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "*"  # temporary for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================
# DATABASE
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# ROOT
# =========================
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


# =========================
# USER CRUD
# =========================
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


# =========================
# ROUTERS (SAFE IMPORT)
# =========================
try:
    from .routes import auth
    app.include_router(auth.router)
    print("Auth router loaded")
except Exception as e:
    print("Auth router failed:", e)


try:
    from .routes import performance
    app.include_router(performance.router)
    print("Performance router loaded")
except Exception as e:
    print("Performance router failed:", e)


try:
    from .routes.ai import router as ai_router
    app.include_router(ai_router, prefix="/ai")
    print("AI router loaded")
except Exception as e:
    print("AI router failed:", e)


# =========================
# VERCEL HANDLER
# =========================
handler = Mangum(app)