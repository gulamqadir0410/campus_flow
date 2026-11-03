
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.academics.models import (
        ClassTeacherAssignment,
        TeachingAssignment,
    )

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_number: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    hire_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    employment_status: Mapped[str] = mapped_column(
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

    class_teacher_assignments: Mapped[
        list["ClassTeacherAssignment"]
    ] = relationship(back_populates="teacher")

    teaching_assignments: Mapped[
        list["TeachingAssignment"]
    ] = relationship(back_populates="teacher")
