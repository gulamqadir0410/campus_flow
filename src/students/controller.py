from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src.students.schemas import StudentCreate, StudentUpdate
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

def get_all_students(page:int, limit:int,db:Session):

    offset = (page - 1) * limit

    total_students = db.query(Student).count()

    students = (
        db.query(Student)
        .order_by(Student.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total_students + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_students": total_students,
        "total_pages": total_pages,
        "students": students
    }

def get_student_by_id(student_id:int,db:Session):
    one_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not one_student:
        raise HTTPException(404, detail=f"Student With ID: {student_id} Not Found.")

    return one_student

def get_student_by_admission_num(admission_num:str,db:Session):
    one_student = db.query(Student).filter(
        Student.admission_number == admission_num
    ).first()

    if not one_student:
        raise HTTPException(404, detail=f"Student With Admission Number: {admission_num} Not Found.")

    return one_student

def update_student(admission_num:str, body:StudentUpdate, db:Session):

    one_student = db.query(Student).filter(
        Student.admission_number == admission_num
    ).first()

    if not one_student:
        raise HTTPException(404, detail=f"Student With Admission Number: {admission_num} Not Found.")

    body = body.model_dump(exclude_unset=True)

    for key,val in body.items():
        setattr(one_student, key, val)

    db.add(one_student)
    db.commit()
    db.refresh(one_student)

    return one_student
