"""Honey-token request and response schemas."""

from datetime import datetime
from typing import Any

from pydantic import Field

from app.models.enums import HoneyTokenType
from app.schemas.base import SchemaBase


class HoneyTokenCreate(SchemaBase):
    """Request payload used to create a honey token."""

    project_domain: str = Field(
        min_length=1,
        max_length=253,
        description="Domain of the project that owns the token.",
    )
    token_type: HoneyTokenType = Field(description="Honey-token category.")
    token_value: str = Field(
        min_length=1,
        max_length=512,
        description="Globally unique honey-token value.",
    )
    label: str | None = Field(
        default=None,
        max_length=255,
        description="Optional human-readable token label.",
    )
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Optional structured token metadata.",
    )


class HoneyTokenRevoke(SchemaBase):
    """Request payload used to revoke a honey token."""

    token_value: str = Field(
        min_length=1,
        max_length=512,
        description="Globally unique honey-token value to revoke.",
    )


class HoneyTokenRotate(SchemaBase):
    """Request payload used to rotate a honey token."""

    old_token_value: str = Field(
        min_length=1,
        max_length=512,
        description="Existing honey-token value to replace.",
    )
    new_token_value: str = Field(
        min_length=1,
        max_length=512,
        description="New globally unique honey-token value.",
    )


class HoneyTokenResponse(SchemaBase):
    """Honey-token representation returned by the API."""

    id: int = Field(description="Honey-token database identifier.")
    project_id: int = Field(description="Identifier of the owning project.")
    token_type: HoneyTokenType = Field(description="Honey-token category.")
    token_value: str = Field(description="Globally unique honey-token value.")
    label: str | None = Field(description="Optional human-readable token label.")
    metadata: dict[str, Any] | None = Field(
        validation_alias="token_metadata",
        description="Optional structured token metadata.",
    )
    is_active: bool = Field(description="Whether the token is active.")
    created_at: datetime = Field(description="Token creation timestamp.")
    updated_at: datetime = Field(description="Token last-update timestamp.")
