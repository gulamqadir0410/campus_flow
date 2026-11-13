from fastapi import FastAPI


# Register all SQLAlchemy models
from src.students import models as student_models
from src.teachers import models as teacher_models
from src.academics import models as academic_models

from src.students.router import student_routes
from src.enrollments.router import enrollments_routes
from src.academics.router import academics_routes
app = FastAPI(
    title="CampusFlow API",
    description="School Management System API",
    version="1.0.0",
)

app.include_router(student_routes)
app.include_router(enrollments_routes)
app.include_router(academics_routes)
@app.get("/")
def root():
    return {
        "message": "Welcome to CampusFlow",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

