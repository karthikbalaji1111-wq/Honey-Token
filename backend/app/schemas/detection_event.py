"""Detection-event request and response schemas."""

from datetime import datetime
from typing import Any

from pydantic import Field

from app.models.enums import EventSeverity
from app.schemas.base import SchemaBase


class DetectionEventCreate(SchemaBase):
    """Request payload used to record a detection event."""

    token_value: str = Field(
        min_length=1,
        max_length=512,
        description="Globally unique honey-token value that was triggered.",
    )
    ip_address: str = Field(
        min_length=1,
        max_length=45,
        description="Source IP address observed for the event.",
    )
    request_path: str = Field(
        min_length=1,
        description="Request path observed during the event.",
    )
    http_method: str = Field(
        min_length=1,
        max_length=10,
        description="HTTP method observed during the event.",
    )
    severity: EventSeverity = Field(description="Classified event severity.")
    user_agent: str | None = Field(
        default=None,
        description="Optional request user-agent value.",
    )
    headers: dict[str, Any] | None = Field(
        default=None,
        description="Optional captured request headers.",
    )


class DetectionEventResponse(SchemaBase):
    """Detection-event representation returned by the API."""

    id: int = Field(description="Detection-event database identifier.")
    honey_token_id: int = Field(description="Identifier of the triggered honey token.")
    ip_address: str = Field(description="Source IP address observed for the event.")
    user_agent: str | None = Field(description="Optional request user-agent value.")
    request_path: str = Field(description="Request path observed during the event.")
    http_method: str = Field(description="HTTP method observed during the event.")
    headers: dict[str, Any] | None = Field(description="Captured request headers.")
    severity: EventSeverity = Field(description="Classified event severity.")
    triggered_at: datetime = Field(description="Time at which the event was triggered.")
    created_at: datetime = Field(description="Event persistence timestamp.")


class DetectionEventStatisticsResponse(SchemaBase):
    """Aggregated detection-event counts."""

    total_events: int = Field(description="Total number of recorded events.")
    today_events: int = Field(description="Number of events recorded today in UTC.")
