from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import HoneyTokenType
from app.models.honey_token import HoneyToken
from app.repositories.base import BaseRepository


class HoneyTokenRepository(BaseRepository[HoneyToken]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, HoneyToken)

    def get_by_token(self, token_value: str) -> HoneyToken | None:
        stmt = select(HoneyToken).where(HoneyToken.token_value == token_value)
        return self.session.scalar(stmt)

    def list_by_project(self, project_id: int) -> list[HoneyToken]:
        stmt = select(HoneyToken).where(HoneyToken.project_id == project_id)
        return list(self.session.scalars(stmt).all())

    def list_active(self, project_id: int | None = None) -> list[HoneyToken]:
        stmt = select(HoneyToken).where(HoneyToken.is_active.is_(True))
        if project_id is not None:
            stmt = stmt.where(HoneyToken.project_id == project_id)
        return list(self.session.scalars(stmt).all())

    def list_by_type(self, token_type: HoneyTokenType, project_id: int | None = None) -> list[HoneyToken]:
        stmt = select(HoneyToken).where(HoneyToken.token_type == token_type)
        if project_id is not None:
            stmt = stmt.where(HoneyToken.project_id == project_id)
        return list(self.session.scalars(stmt).all())
