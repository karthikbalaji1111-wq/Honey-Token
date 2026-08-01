"""Shared service-layer functionality."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import ValidationError


class BaseService:
    """Provide shared dependencies and validation for domain services."""

    def __init__(self, session: Session) -> None:
        """Initialize the service with its transaction session.

        Args:
            session: The SQLAlchemy session shared by the service repositories.

        Returns:
            None.
        """
        self.session = session

    @staticmethod
    def _validate_required_fields(*fields: tuple[str, str | None]) -> None:
        """Raise a validation error when named string fields are blank.

        Args:
            fields: Pairs containing a display name and its string value.

        Returns:
            None.

        Raises:
            ValidationError: If one or more field values are blank.
        """
        missing_fields = [
            field_name
            for field_name, value in fields
            if value is None or not value.strip()
        ]
        if not missing_fields:
            return

        verb = "is" if len(missing_fields) == 1 else "are"
        field_names = " and ".join(missing_fields)
        raise ValidationError(f"{field_names} {verb} required")
