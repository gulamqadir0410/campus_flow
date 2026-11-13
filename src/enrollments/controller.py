from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.students.models import Student
from src.academics.models import SchoolClass
from src.students.models import StudentEnrollment
from src.enrollments.schemas import EnrollmentCreate


def create_enrollment(body: EnrollmentCreate, db: Session):

    # 1. Check whether the student exists
    existing_student = db.get(Student, body.student_id)

    if not existing_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student ID {body.student_id} does not exist"
        )

    # 2. Check whether the class exists
    existing_class = db.get(SchoolClass, body.school_class_id)

    if not existing_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class ID {body.school_class_id} does not exist"
        )

    # 3. Check whether the student already has an active enrollment
    existing_enrollment = db.query(StudentEnrollment).filter(
        StudentEnrollment.student_id == body.student_id,
        StudentEnrollment.status == "active"
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student already has an active enrollment"
        )

    # 4. Check manual roll-number availability
    if body.roll_number is not None:

        existing_roll = db.query(StudentEnrollment).filter(
            StudentEnrollment.school_class_id == body.school_class_id,
            StudentEnrollment.roll_number == body.roll_number,
            StudentEnrollment.status == "active"
        ).first()

        if existing_roll:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Roll number already assigned in this class"
            )

        assigned_roll_number = body.roll_number

    else:
        # 5. Automatically find the highest active roll number
        highest_roll = db.query(
            func.max(StudentEnrollment.roll_number)
        ).filter(
            StudentEnrollment.school_class_id == body.school_class_id,
            StudentEnrollment.status == "active"
        ).scalar()

        # If no students exist, start from 1; otherwise increment
        assigned_roll_number = (highest_roll or 0) + 1

    # 6. Prepare enrollment data
    enrollment_data = body.model_dump(exclude_unset=True)

    # Override roll_number with the manually selected or generated number
    enrollment_data["roll_number"] = assigned_roll_number

    # 7. Create enrollment object
    new_enrollment = StudentEnrollment(**enrollment_data)

    try:
        db.add(new_enrollment)
        db.commit()
        db.refresh(new_enrollment)

        return new_enrollment

    except Exception:
        db.rollback()
        raise