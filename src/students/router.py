
from fastapi import APIRouter, Depends, status, Query
from src.students import  controller
from src.students.schemas import StudentCreate, StudentUpdate, StudentStatusUpdate
from src.utils.db import get_db
from sqlalchemy.orm import Session

student_routes = APIRouter(prefix="/students")

@student_routes.post("/create", status_code=status.HTTP_201_CREATED)
def create_student(body:StudentCreate, db:Session = Depends(get_db) ):
    return controller.create_student(body,db)

@student_routes.get("/all", status_code=status.HTTP_200_OK)
def get_all_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return controller.get_all_students(page, limit, db)

@student_routes.get("/{student_id}", status_code= status.HTTP_200_OK)
def get_student_by_id(student_id:int, db:Session = Depends(get_db)):
    return controller.get_student_by_id(student_id,db)

@student_routes.get("/admission/{admission_num}", status_code= status.HTTP_200_OK)
def get_student_by_admission_num(admission_num:str,db:Session = Depends(get_db)):
    return controller.get_student_by_admission_num(admission_num,db)

@student_routes.put("/update_student/{admission_num}", status_code= status.HTTP_200_OK)
def update_student(admission_num:str,body:StudentUpdate, db:Session = Depends(get_db)):
    return controller.update_student(admission_num, body, db)


@student_routes.patch("/{student_id}/status",status_code=status.HTTP_200_OK)
def student_status_set(student_id: int,body:StudentStatusUpdate ,db:Session = Depends(get_db)):
    return controller.student_status_set(student_id,body, db)
