
from __future__ import annotations

from datetime import date

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.db import Base


class AcademicSession(Base):
    __tablename__ = "academic_sessions"

    __table_args__ = (
        CheckConstraint(
            "start_date < end_date",
            name="ck_session_dates",
        ),
        Index(
            "uq_active_academic_session",
            "is_active",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    classes: Mapped[list["SchoolClass"]] = relationship(
        back_populates="academic_session"
    )


class ClassLevel(Base):
    __tablename__ = "class_levels"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )

    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    classes: Mapped[list["SchoolClass"]] = relationship(
        back_populates="class_level"
    )


class SchoolClass(Base):
    __tablename__ = "school_classes"

    __table_args__ = (
        UniqueConstraint(
            "academic_session_id",
            "class_level_id",
            "section_name",
            name="uq_session_class_section",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    academic_session_id: Mapped[int] = mapped_column(
        ForeignKey("academic_sessions.id"), nullable=False
    )

    class_level_id: Mapped[int] = mapped_column(
        ForeignKey("class_levels.id"), nullable=False
    )

    section_name: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    capacity: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    academic_session: Mapped["AcademicSession"] = relationship(
        back_populates="classes"
    )

    class_level: Mapped["ClassLevel"] = relationship(
        back_populates="classes"
    )

    enrollments: Mapped[list["StudentEnrollment"]] = relationship(
        back_populates="school_class"
    )

    class_teacher_assignments: Mapped[
        list["ClassTeacherAssignment"]
    ] = relationship(back_populates="school_class")

    teaching_assignments: Mapped[
        list["TeachingAssignment"]
    ] = relationship(back_populates="school_class")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    teaching_assignments: Mapped[
        list["TeachingAssignment"]
    ] = relationship(back_populates="subject")


class ClassTeacherAssignment(Base):
    __tablename__ = "class_teacher_assignments"

    __table_args__ = (
        Index(
            "uq_active_class_teacher",
            "school_class_id",
            unique=True,
            postgresql_where=text("end_date IS NULL"),
        ),
        CheckConstraint(
            "end_date IS NULL OR start_date <= end_date",
            name="ck_class_teacher_dates",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    school_class_id: Mapped[int] = mapped_column(
        ForeignKey("school_classes.id"), nullable=False
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"), nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )

    end_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    school_class: Mapped["SchoolClass"] = relationship(
        back_populates="class_teacher_assignments"
    )

    teacher: Mapped["Teacher"] = relationship(
        back_populates="class_teacher_assignments"
    )


class TeachingAssignment(Base):
    __tablename__ = "teaching_assignments"

    __table_args__ = (
        Index(
            "uq_active_teaching_assignment",
            "teacher_id",
            "school_class_id",
            "subject_id",
            unique=True,
            postgresql_where=text("end_date IS NULL"),
        ),
        CheckConstraint(
            "end_date IS NULL OR start_date <= end_date",
            name="ck_teaching_assignment_dates",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"), nullable=False
    )

    school_class_id: Mapped[int] = mapped_column(
        ForeignKey("school_classes.id"), nullable=False
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"), nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )

    end_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    school_class: Mapped["SchoolClass"] = relationship(
        back_populates="teaching_assignments"
    )

    teacher: Mapped["Teacher"] = relationship(
        back_populates="teaching_assignments"
    )

    subject: Mapped["Subject"] = relationship(
        back_populates="teaching_assignments"
    )
