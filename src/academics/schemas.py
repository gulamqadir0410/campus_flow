from datetime import date

from pydantic import BaseModel, Field, ConfigDict

class AcademicSessionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    start_date: date
    end_date: date
    is_active: bool = False

class AcademicSessionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=30)
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None

class AcademicSessionResponse(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ClassLevelCreate(BaseModel):

    name: str = Field(min_length=1, max_length=30)
    code: str
    sort_order: int
    is_active: bool = True

class ClassLevelUpdate(BaseModel):

    name: str | None = Field(default=None,min_length=1, max_length=30)
    code: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None

class ClassLevelResponse(BaseModel):

    id: int
    name: str
    code: str
    sort_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class SchoolClassCreate(BaseModel):

    academic_session_id: int
    class_level_id: int
    section_name: str
    capacity:int | None = None

class SchoolClassUpdate(BaseModel):

    academic_session_id: int | None = None
    class_level_id: int | None = None
    section_name: str | None = None
    capacity: int | None = None

class SchoolClassResponse(BaseModel):

    id:int
    academic_session_id: int
    class_level_id: int
    section_name: str
    capacity: int | None

    model_config = ConfigDict(from_attributes=True)