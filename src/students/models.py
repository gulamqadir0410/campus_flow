
from __future__ import annotations
from sqlalchemy import func

from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.db import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    admission_number: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    gender: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    enrollments: Mapped[list["StudentEnrollment"]] = relationship(
        back_populates="student"
    )


class StudentEnrollment(Base):
    __tablename__ = "student_enrollments"

    __table_args__ = (
        Index(
            "uq_student_current_enrollment",
            "student_id",
            unique=True,
            postgresql_where=text("left_at IS NULL"),
        ),
        CheckConstraint(
            "left_at IS NULL OR enrolled_at <= left_at",
            name="ck_enrollment_dates",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"), nullable=False
    )

    school_class_id: Mapped[int] = mapped_column(
        ForeignKey("school_classes.id"), nullable=False
    )

    roll_number: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )

    enrolled_at: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )

    left_at: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )

    student: Mapped["Student"] = relationship(
        back_populates="enrollments"
    )

    school_class: Mapped["SchoolClass"] = relationship(
        back_populates="enrollments"
    )
