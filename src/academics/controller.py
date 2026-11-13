
from src.academics.models import AcademicSession, SchoolClass, ClassLevel, ClassTeacherAssignment, TeachingAssignment,Subject
from src.academics.schemas import AcademicSessionCreate, AcademicSessionUpdate, ClassLevelCreate, ClassLevelUpdate, \
    SchoolClassCreate, SchoolClassUpdate, SubjectCreate, SubjectUpdate
from src.students.models import StudentEnrollment
from sqlalchemy.orm import Session
from fastapi import HTTPException


#academics controllers

def create_academic_session(body:AcademicSessionCreate, db:Session):

    session_name = db.query(AcademicSession).filter(
        AcademicSession.name == body.name
    ).first()

    if session_name:
        raise HTTPException(409, detail=f"Session name '{body.name}' already exists.")

    if body.is_active:
        active_session = db.query(AcademicSession).filter(
            AcademicSession.is_active.is_(True)
        ).first()

        if active_session:
            raise HTTPException(409, detail="Another academic session is already active.")

    new_session = AcademicSession(**body.model_dump())

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


def get_all_academic_sessions(db:Session):

    academics_data = db.query(AcademicSession).order_by(
        AcademicSession.start_date.desc()
    ).all()

    return academics_data


def get_academic_session_by_id(session_id:int, db:Session):

    academic_data = db.query(AcademicSession).filter(
        AcademicSession.id == session_id
    ).first()

    if not academic_data:
        raise HTTPException(404, detail=f"Academic session data with id '{session_id}' not found")

    return academic_data


def update_academic_session(body:AcademicSessionUpdate, session_id:int, db:Session):

    existing_session = db.query(AcademicSession).filter(
        AcademicSession.id == session_id
    ).first()

    if not existing_session:
        raise HTTPException(404, detail=f"Academic session data with id '{session_id}' not found")

    update_data = body.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(422, detail="Update fields cannot be null.")

    if "name" in update_data:
        existing_name = db.query(AcademicSession).filter(
            AcademicSession.name == update_data["name"],
            AcademicSession.id != session_id
        ).first()

        if existing_name:
            raise HTTPException(409, detail="Academic session name already exists.")

    start_date = update_data.get("start_date", existing_session.start_date)
    end_date = update_data.get("end_date", existing_session.end_date)

    if start_date >= end_date:
        raise HTTPException(422, detail="Start date must be before end date.")

    if update_data.get("is_active") is True:
        active_session = db.query(AcademicSession).filter(
            AcademicSession.is_active.is_(True),
            AcademicSession.id != session_id
        ).first()

        if active_session:
            raise HTTPException(409, detail="Another academic session is already active. Deactivate it first.")

    for key,val in update_data.items():
        setattr(existing_session,key,val)

    db.add(existing_session)
    db.commit()
    db.refresh(existing_session)

    return existing_session


def delete_academic_session(session_id:int, db:Session):

    existing_session = db.query(AcademicSession).filter(
        AcademicSession.id == session_id
    ).first()

    if not existing_session:
        raise HTTPException(404, detail=f"Academic session data with id '{session_id}' not found")

    existing_class = db.query(SchoolClass).filter(
        SchoolClass.academic_session_id == session_id
    ).first()

    if existing_class:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete session because classes are associated with it."
        )

    db.delete(existing_session)
    db.commit()

    return None


#class level controllers

def create_class_level(body:ClassLevelCreate, db:Session):

    existing_name = db.query(ClassLevel).filter(
        ClassLevel.name == body.name
    ).first()

    if existing_name:
        raise HTTPException(409, detail=f"Class name '{body.name}' already exists.")

    existing_code = db.query(ClassLevel).filter(
        ClassLevel.code == body.code
    ).first()

    if existing_code:
        raise HTTPException(409, detail=f"Class code '{body.code}' already exists.")

    new_class_level = ClassLevel(**body.model_dump())

    db.add(new_class_level)
    db.commit()
    db.refresh(new_class_level)

    return new_class_level


def get_class_level(db:Session):

    class_data = db.query(ClassLevel).all()

    return class_data


def get_class_level_by_id(class_level_id:int,db:Session):

    existing_class_level = db.query(ClassLevel).filter(
        ClassLevel.id == class_level_id
    ).first()

    if not existing_class_level:
        raise HTTPException(404, detail=f"Class level with id {class_level_id} does not exist")

    return existing_class_level


def update_class_level(class_level_id:int, body:ClassLevelUpdate, db:Session):

    existing_class_level = db.query(ClassLevel).filter(
        ClassLevel.id == class_level_id
    ).first()

    if not existing_class_level:
        raise HTTPException(404, detail=f"Class Level with id {class_level_id} not found")

    update_data = body.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(422, detail="Update fields cannot be null.")

    if "name" in update_data:
        existing_name = db.query(ClassLevel).filter(
            ClassLevel.name == update_data["name"],
            ClassLevel.id != class_level_id
        ).first()

        if existing_name:
            raise HTTPException(409, detail="Class name already exists.")

    if "code" in update_data:
        existing_code = db.query(ClassLevel).filter(
            ClassLevel.code == update_data["code"],
            ClassLevel.id != class_level_id
        ).first()

        if existing_code:
            raise HTTPException(409, detail="Class code already exists.")

    for key,val in update_data.items():
        setattr(existing_class_level, key,val)

    db.add(existing_class_level)
    db.commit()
    db.refresh(existing_class_level)

    return existing_class_level


def delete_class_level(class_level_id:int, db:Session):

    existing_class_level = db.query(ClassLevel).filter(
        ClassLevel.id == class_level_id
    ).first()

    if not existing_class_level:
        raise HTTPException(404, detail=f"Class Level with id {class_level_id} not found")

    existing_class = db.query(SchoolClass).filter(
        SchoolClass.class_level_id == class_level_id
    ).first()

    if existing_class:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete class level because classes are associated with it."
        )

    db.delete(existing_class_level)
    db.commit()

    return None


# School Class controllers

def create_school_class(body:SchoolClassCreate, db:Session):

    existing_session = db.query(AcademicSession).filter(
        AcademicSession.id == body.academic_session_id
    ).first()

    if not existing_session:
        raise HTTPException(404, detail=f"Academic session with id {body.academic_session_id} not found.")

    existing_level = db.query(ClassLevel).filter(
        ClassLevel.id == body.class_level_id
    ).first()

    if not existing_level:
        raise HTTPException(404, detail=f"Class level with id {body.class_level_id} not found.")

    existing_school_class = db.query(SchoolClass).filter(
        SchoolClass.academic_session_id == body.academic_session_id,
        SchoolClass.class_level_id == body.class_level_id,
        SchoolClass.section_name == body.section_name
    ).first()

    if existing_school_class:
        raise HTTPException(409, detail=f"Section '{body.section_name}' already exists for this class level in this academic session")

    new_school_class = SchoolClass(**body.model_dump())

    db.add(new_school_class)
    db.commit()
    db.refresh(new_school_class)

    return new_school_class


def get_school_class(db:Session):

    existing_school_class = db.query(SchoolClass).all()

    return existing_school_class


def get_school_class_by_id(school_class_id:int, db:Session):

    existing_school_class = db.query(SchoolClass).filter(
        SchoolClass.id == school_class_id
    ).first()

    if not existing_school_class:
        raise HTTPException(404, detail=f"No school class record with id {school_class_id} found")

    return existing_school_class


def update_school_class(school_class_id:int, body:SchoolClassUpdate, db:Session):

    existing_school_class = db.query(SchoolClass).filter(
        SchoolClass.id == school_class_id
    ).first()

    if not existing_school_class:
        raise HTTPException(404, detail=f"No school class record with id {school_class_id} found")

    update_data = body.model_dump(exclude_unset=True)

    if "academic_session_id" in update_data:
        if update_data["academic_session_id"] is None:
            raise HTTPException(422, detail="Academic session ID cannot be null.")

        existing_session = db.query(AcademicSession).filter(
            AcademicSession.id == update_data["academic_session_id"]
        ).first()

        if not existing_session:
            raise HTTPException(404, detail="Academic session not found.")

    if "class_level_id" in update_data:
        if update_data["class_level_id"] is None:
            raise HTTPException(422, detail="Class level ID cannot be null.")

        existing_level = db.query(ClassLevel).filter(
            ClassLevel.id == update_data["class_level_id"]
        ).first()

        if not existing_level:
            raise HTTPException(404, detail="Class level not found.")

    if "section_name" in update_data and update_data["section_name"] is None:
        raise HTTPException(422, detail="Section name cannot be null.")

    session_id = update_data.get("academic_session_id", existing_school_class.academic_session_id)
    level_id = update_data.get("class_level_id", existing_school_class.class_level_id)
    section_name = update_data.get("section_name", existing_school_class.section_name)

    duplicate_class = db.query(SchoolClass).filter(
        SchoolClass.academic_session_id == session_id,
        SchoolClass.class_level_id == level_id,
        SchoolClass.section_name == section_name,
        SchoolClass.id != school_class_id
    ).first()

    if duplicate_class:
        raise HTTPException(409, detail="This school class section already exists.")

    changing_class_identity = (
        session_id != existing_school_class.academic_session_id
        or level_id != existing_school_class.class_level_id
    )

    if changing_class_identity:

        existing_enrollment = db.query(StudentEnrollment).filter(
            StudentEnrollment.school_class_id == school_class_id
        ).first()

        existing_class_teacher = db.query(ClassTeacherAssignment).filter(
            ClassTeacherAssignment.school_class_id == school_class_id
        ).first()

        existing_teaching_assignment = db.query(TeachingAssignment).filter(
            TeachingAssignment.school_class_id == school_class_id
        ).first()

        if existing_enrollment or existing_class_teacher or existing_teaching_assignment:
            raise HTTPException(
                status_code=409,
                detail="Cannot change academic session or class level because enrollment or teacher assignment history exists."
            )

    for key,val in update_data.items():
        setattr(existing_school_class,key,val)

    db.add(existing_school_class)
    db.commit()
    db.refresh(existing_school_class)

    return existing_school_class


def delete_school_class(school_class_id:int, db:Session):

    existing_school_class = db.query(SchoolClass).filter(
        SchoolClass.id == school_class_id
    ).first()

    if not existing_school_class:
        raise HTTPException(404, detail=f"No school class record with id {school_class_id} found")

    existing_enrollment = db.query(StudentEnrollment).filter(
        StudentEnrollment.school_class_id == school_class_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete school class because associated student enrollment records exist."
        )

    existing_class_teacher = db.query(ClassTeacherAssignment).filter(
        ClassTeacherAssignment.school_class_id == school_class_id
    ).first()

    if existing_class_teacher:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete school class because associated class teacher records exist."
        )

    existing_teaching_assignment = db.query(TeachingAssignment).filter(
        TeachingAssignment.school_class_id == school_class_id
    ).first()

    if existing_teaching_assignment:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete school class because associated teaching assignment records exist."
        )

    db.delete(existing_school_class)
    db.commit()

    return None


# Subject Controllers

def create_subject(body:SubjectCreate, db:Session):

    existing_subject = db.query(Subject).filter(
        Subject.name == body.name
    ).first()

    if existing_subject:
        raise HTTPException(409, detail="Subject already exists")

    existing_code = db.query(Subject).filter(
        Subject.code == body.code
    ).first()

    if existing_code:
        raise HTTPException(409, detail="Subject code exists")

    new_subject = Subject(**body.model_dump())

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

def get_all_subjects(db:Session):

    all_subjects = db.query(Subject).all()

    return all_subjects

def get_subject_by_id(subject_id:int, db:Session):

    existing_subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not existing_subject:
        raise HTTPException(404, detail=f"Subject with id {subject_id} not found")

    return existing_subject

def update_subject_by_id(body:SubjectUpdate,subject_id:int, db:Session):

    existing_subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not existing_subject:
        raise HTTPException(404, detail=f"Subject with id {subject_id} not found")

    updated_subject_data = body.model_dump(exclude_unset=True)

    for field in ["name","code","is_active"]:
        if field in updated_subject_data and updated_subject_data[field] is None:
            raise HTTPException(422, detail="Update fields cannot be null.")

    # 4. Check whether the new name is already used
    if "name" in updated_subject_data:
        existing_name = db.query(Subject).filter(
            Subject.name == updated_subject_data["name"],
            Subject.id != subject_id
        ).first()

        if existing_name:
            raise HTTPException(409, detail="Subject name already exists")

    # 5. Check whether the new code is already used
    if "code" in updated_subject_data:
        existing_code = db.query(Subject).filter(
            Subject.code == updated_subject_data["code"],
            Subject.id != subject_id
        ).first()

        if existing_code:
            raise HTTPException(409, detail="Subject code already exists")

    for key,val in updated_subject_data.items():
        setattr(existing_subject,key,val)

    db.add(existing_subject)
    db.commit()
    db.refresh(existing_subject)

    return existing_subject

def delete_subject(subject_id:int,db:Session):

    existing_subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not existing_subject:
        raise HTTPException(404, detail=f"Subject with id {subject_id} not found")

    existing_assignment = db.query(TeachingAssignment).filter(
        TeachingAssignment.subject_id == subject_id
    ).first()

    if existing_assignment:
        raise HTTPException(409, detail="Subject is assigned cannot delete")

    db.delete(existing_subject)
    db.commit()

    return None