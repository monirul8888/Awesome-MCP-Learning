from fastapi import FastAPI
from app.database import engine, Base
from app.api.routes import router

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title       = "Student Expense Tracker API",
    description = "Track your daily expenses as a student",
    version     = "1.0.0",
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Student Expense Tracker is running 🎓"}