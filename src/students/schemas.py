from datetime import date
from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    admission_number: str = Field(min_length=1, max_length=30)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date | None = None
    gender: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None