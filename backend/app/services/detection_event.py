from __future__ import annotations
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import HoneyTokenNotFoundError, ValidationError
from app.models.detection_event import DetectionEvent
from app.models.enums import EventSeverity
from app.repositories.detection_event import DetectionEventRepository
from app.repositories.honey_token import HoneyTokenRepository
from app.services.base import BaseService


class DetectionEventService(BaseService):
    def __init__(
        self, session: Session, event_repo: DetectionEventRepository, token_repo: HoneyTokenRepository
    ) -> None:
        super().__init__(session)
        self.event_repo = event_repo
        self.token_repo = token_repo

    def _resolve_token_id(self, token_value: str | None) -> int | None:
        if not token_value:
            return None
        token = self.token_repo.get_by_token(token_value)
        if not token:
            raise HoneyTokenNotFoundError(f"Token '{token_value}' not found")
        return token.id

    def record_event(
        self, token_value: str, ip_address: str, request_path: str, http_method: str, 
        severity: EventSeverity, user_agent: str | None = None, headers: dict[str, Any] | None = None
    ) -> DetectionEvent:
        if not ip_address or not request_path or not http_method:
            raise ValidationError("IP address, request path, and HTTP method are required")

        token_id = self._resolve_token_id(token_value)
        if token_id is None:
            raise ValidationError("Token value is required for recording events")

        event = self.event_repo.create(
            honey_token_id=token_id,
            ip_address=ip_address,
            request_path=request_path,
            http_method=http_method,
            severity=severity,
            user_agent=user_agent,
            headers=headers,
        )
        try:
            self.session.commit()
            return event
        except Exception:
            self.session.rollback()
            raise

    def list_recent_events(self, token_value: str | None = None, limit: int = 100) -> list[DetectionEvent]:
        honey_token_id = self._resolve_token_id(token_value)
        return self.event_repo.list_recent(honey_token_id=honey_token_id, limit=limit)

    def count_today(self, token_value: str | None = None) -> int:
        honey_token_id = self._resolve_token_id(token_value)
        return self.event_repo.count_today(honey_token_id=honey_token_id)

    def get_statistics(self) -> dict[str, int]:
        """Returns high-level statistics of detection events."""
        total_events = self.event_repo.count()
        today_events = self.event_repo.count_today()
        
        return {
            "total_events": total_events,
            "today_events": today_events,
        }
