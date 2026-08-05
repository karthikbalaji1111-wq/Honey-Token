from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model_class: type[ModelType]) -> None:
        self.session = session
        self.model_class = model_class

    def create(self, **kwargs: Any) -> ModelType:
        obj = self.model_class(**kwargs)
        self.session.add(obj)
        return obj

    def get_by_id(self, id: int) -> ModelType | None:
        return self.session.get(self.model_class, id)

    def list(self) -> list[ModelType]:
        stmt = select(self.model_class)
        return list(self.session.scalars(stmt).all())

    def exists(self, id: int) -> bool:
        stmt = select(func.count()).select_from(self.model_class).where(getattr(self.model_class, "id") == id)
        return (self.session.scalar(stmt) or 0) > 0

    def count(self) -> int:
        stmt = select(func.count()).select_from(self.model_class)
        return self.session.scalar(stmt) or 0

    def delete(self, id: int) -> None:
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)

    def flush(self) -> None:
        self.session.flush()

    def refresh(self, obj: ModelType) -> None:
        self.session.refresh(obj)
