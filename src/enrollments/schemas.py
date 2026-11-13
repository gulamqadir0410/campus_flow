from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    school_class_id: int
    roll_number: int | None = None

