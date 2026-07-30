from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ApplicationConfig(BaseModel):
    __tablename__ = "application_configs"

    key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
