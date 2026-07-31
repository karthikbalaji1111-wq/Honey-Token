from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.detection_event import DetectionEvent
from app.repositories.base import BaseRepository


class DetectionEventRepository(BaseRepository[DetectionEvent]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetectionEvent)

    def list_recent(self, honey_token_id: int | None = None, limit: int = 100) -> list[DetectionEvent]:
        stmt = select(DetectionEvent)
        if honey_token_id is not None:
            stmt = stmt.where(DetectionEvent.honey_token_id == honey_token_id)
        stmt = stmt.order_by(DetectionEvent.triggered_at.desc()).limit(limit)
        return list(self.session.scalars(stmt).all())

    def list_between(
        self, honey_token_id: int, start_time: datetime, end_time: datetime
    ) -> list[DetectionEvent]:
        stmt = (
            select(DetectionEvent)
            .where(DetectionEvent.honey_token_id == honey_token_id)
            .where(DetectionEvent.triggered_at >= start_time)
            .where(DetectionEvent.triggered_at <= end_time)
            .order_by(DetectionEvent.triggered_at.desc())
        )
        return list(self.session.scalars(stmt).all())

    def find_by_ip(self, ip_address: str, limit: int = 100) -> list[DetectionEvent]:
        stmt = (
            select(DetectionEvent)
            .where(DetectionEvent.ip_address == ip_address)
            .order_by(DetectionEvent.triggered_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def count_today(self, honey_token_id: int | None = None) -> int:
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(func.count())
            .select_from(DetectionEvent)
            .where(DetectionEvent.triggered_at >= start_of_day)
        )
        if honey_token_id is not None:
            stmt = stmt.where(DetectionEvent.honey_token_id == honey_token_id)
        return self.session.scalar(stmt) or 0
