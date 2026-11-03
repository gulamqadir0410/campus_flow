from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.students.schemas import StudentCreate
from src.students.models import Student


def create_student(body: StudentCreate, db: Session):

    # 1. Check duplicate admission number
    existing_student = db.query(Student).filter(
        Student.admission_number == body.admission_number
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admission number already exists"
        )

    # 2. Check duplicate email (only if email is provided)
    if body.email:
        existing_email = db.query(Student).filter(
            Student.email == body.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

    # 3. Create student
    new_student = Student(**body.model_dump())

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student record conflicts with existing data"
        )