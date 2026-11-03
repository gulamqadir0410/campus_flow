
from fastapi import APIRouter, Depends, status
from src.students import  controller
from src.students.schemas import StudentCreate
from src.utils.db import get_db
from sqlalchemy.orm import Session

student_routes = APIRouter(prefix="/students")

@student_routes.post("/create", status_code=status.HTTP_201_CREATED)
def create_student(body:StudentCreate, db:Session = Depends(get_db) ):
    return controller.create_student(body,db)