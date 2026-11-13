from fastapi import APIRouter
from src.academics import controller
from src.utils.db import get_db
from src.academics.schemas import AcademicSessionCreate, AcademicSessionResponse, AcademicSessionUpdate, \
    ClassLevelCreate, ClassLevelResponse, ClassLevelUpdate, SchoolClassCreate, SchoolClassUpdate, SchoolClassResponse, \
    SubjectResponse, SubjectCreate, SubjectUpdate
from sqlalchemy.orm import Session
from fastapi import Depends,status

academics_routes = APIRouter(prefix="/academics")


@academics_routes.post("/sessions", status_code=status.HTTP_201_CREATED, response_model=AcademicSessionResponse)
def create_academic_session(body:AcademicSessionCreate ,db:Session = Depends(get_db)):
    return controller.create_academic_session(body, db)

@academics_routes.get("/sessions", status_code=status.HTTP_200_OK, response_model=list[AcademicSessionResponse])
def get_all_academic_sessions(db:Session = Depends(get_db)):
    return controller.get_all_academic_sessions(db)

@academics_routes.get("/sessions/{session_id}", status_code=status.HTTP_200_OK, response_model=AcademicSessionResponse)
def get_academic_session_by_id(session_id:int, db:Session = Depends(get_db)):
    return controller.get_academic_session_by_id(session_id, db)

@academics_routes.patch("/sessions/{session_id}", status_code=status.HTTP_200_OK, response_model=AcademicSessionResponse)
def update_academic_session(body:AcademicSessionUpdate,session_id:int, db:Session = Depends(get_db)):
    return controller.update_academic_session(body, session_id, db)

@academics_routes.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_academic_session(session_id:int,db:Session = Depends(get_db)):
    return controller.delete_academic_session(session_id, db)

# Class Level Routes

@academics_routes.post("/class-levels", status_code=status.HTTP_201_CREATED, response_model=ClassLevelResponse)
def create_class_level(body:ClassLevelCreate, db:Session = Depends(get_db)):
    return controller.create_class_level(body, db)

@academics_routes.get("/class-levels",response_model=list[ClassLevelResponse], status_code=status.HTTP_200_OK)
def get_class_level(db:Session = Depends(get_db)):
    return controller.get_class_level(db)

@academics_routes.get("/class-levels/{class_level_id}", response_model=ClassLevelResponse, status_code=status.HTTP_200_OK)
def get_class_level_by_id(class_level_id:int, db:Session = Depends(get_db)):
    return controller.get_class_level_by_id(class_level_id, db)

@academics_routes.patch("/class-levels/{class_level_id}", response_model=ClassLevelResponse, status_code=status.HTTP_200_OK)
def update_class_level(class_level_id:int,body:ClassLevelUpdate ,db:Session = Depends(get_db)):
    return controller.update_class_level(class_level_id, body, db)

@academics_routes.delete("/class-levels/{class_level_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_level(class_level_id:int, db:Session = Depends(get_db)):
    return controller.delete_class_level(class_level_id, db)

# School Class Routes

@academics_routes.post("/school-classes",status_code=status.HTTP_201_CREATED ,response_model=SchoolClassResponse)
def create_school_class(body:SchoolClassCreate, db:Session=Depends(get_db)):
    return controller.create_school_class(body, db)

@academics_routes.get("/school-classes",status_code=status.HTTP_200_OK, response_model=list[SchoolClassResponse])
def get_school_class(db:Session=Depends(get_db)):
    return controller.get_school_class(db)

@academics_routes.get("/school-classes/{school_class_id}",status_code=status.HTTP_200_OK, response_model=SchoolClassResponse)
def get_school_class_by_id(school_class_id:int, db:Session=Depends(get_db)):
    return controller.get_school_class_by_id(school_class_id, db)

@academics_routes.patch("/school-classes/{school_class_id}",status_code=status.HTTP_200_OK, response_model=SchoolClassResponse)
def update_school_class(school_class_id:int, body:SchoolClassUpdate, db:Session=Depends(get_db)):
    return controller.update_school_class(school_class_id, body, db)

@academics_routes.delete("/school-classes/{school_class_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_school_class(school_class_id:int, db:Session=Depends(get_db)):
    return controller.delete_school_class(school_class_id, db)

# Subject Routes

@academics_routes.post("/subjects",response_model=SubjectResponse,status_code=status.HTTP_201_CREATED)
def create_subject(body:SubjectCreate, db:Session = Depends(get_db)):
    return controller.create_subject(body, db)

@academics_routes.get("/subjects", response_model= list[SubjectResponse], status_code=status.HTTP_200_OK)
def get_all_subjects(db:Session = Depends(get_db)):
    return controller.get_all_subjects(db)

@academics_routes.get("/subjects/{subject_id}", response_model= SubjectResponse, status_code=status.HTTP_200_OK)
def get_subject_by_id(subject_id:int, db:Session = Depends(get_db)):
    return controller.get_subject_by_id(subject_id,db)

@academics_routes.patch("/subjects/{subject_id}",response_model=SubjectResponse, status_code=status.HTTP_200_OK)
def update_subject_by_id(body:SubjectUpdate,subject_id:int, db:Session = Depends(get_db)):
    return controller.update_subject_by_id(body,subject_id,db)

@academics_routes.delete("/subjects/{subject_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id:int,db:Session = Depends(get_db)):
    return controller.delete_subject(subject_id, db)