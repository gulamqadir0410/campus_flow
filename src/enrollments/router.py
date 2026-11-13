from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.enrollments import controller
from src.enrollments.schemas import EnrollmentCreate
from src.utils.db import get_db

enrollments_routes = APIRouter(prefix="/enrollments")

@enrollments_routes.post("/create",status_code=status.HTTP_201_CREATED)
def create_enrollment(body:EnrollmentCreate, db:Session = Depends(get_db)):
    return controller.create_enrollment(body, db)