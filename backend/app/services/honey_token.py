"""Honey-token service operations."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateHoneyTokenError,
    HoneyTokenNotFoundError,
    ProjectNotFoundError,
)
from app.models.enums import HoneyTokenType
from app.models.honey_token import HoneyToken
from app.repositories.honey_token import HoneyTokenRepository
from app.repositories.project import ProjectRepository
from app.services.base import BaseService


class HoneyTokenService(BaseService):
    """Coordinate honey-token lifecycle operations."""

    def __init__(
        self,
        session: Session,
        token_repo: HoneyTokenRepository,
        project_repo: ProjectRepository,
    ) -> None:
        """Initialize the service with token and project repositories.

        Args:
            session: The transaction session for token operations.
            token_repo: Repository used to persist and retrieve honey tokens.
            project_repo: Repository used to resolve owning projects.

        Returns:
            None.
        """
        super().__init__(session)
        self.token_repo = token_repo
        self.project_repo = project_repo

    def create_token(
        self,
        project_domain: str,
        token_type: HoneyTokenType,
        token_value: str,
        label: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> HoneyToken:
        """Create a unique honey token for an existing project.

        Args:
            project_domain: Domain of the owning project.
            token_type: Category of the honey token.
            token_value: Globally unique value that identifies the token.
            label: Optional human-readable token label.
            metadata: Optional structured token metadata.

        Returns:
            The persisted honey token.

        Raises:
            ValidationError: If a required value is blank.
            ProjectNotFoundError: If the owning project does not exist.
            DuplicateHoneyTokenError: If the token value is already in use.
        """
        self._validate_required_fields(
            ("Project domain", project_domain),
            ("Token value", token_value),
        )

        try:
            project = self.project_repo.get_by_domain(project_domain)
            if not project:
                raise ProjectNotFoundError(f"Project '{project_domain}' not found")

            existing_token = self.token_repo.get_by_token(token_value)
            if existing_token:
                raise DuplicateHoneyTokenError(
                    f"Token with value '{token_value}' already exists"
                )

            token = self.token_repo.create(
                project_id=project.id,
                token_type=token_type,
                token_value=token_value,
                label=label,
                token_metadata=metadata,
            )
            self.session.commit()
            return token
        except Exception:
            self.session.rollback()
            raise

    def revoke_token(self, token_value: str) -> None:
        """Mark an existing honey token as inactive.

        Args:
            token_value: Globally unique value of the token to revoke.

        Returns:
            None.

        Raises:
            ValidationError: If the token value is blank.
            HoneyTokenNotFoundError: If no matching token exists.
        """
        self._validate_required_fields(("Token value", token_value))

        try:
            token = self.token_repo.get_by_token(token_value)
            if not token:
                raise HoneyTokenNotFoundError(f"Token '{token_value}' not found")

            token.is_active = False
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def rotate_token(self, old_token_value: str, new_token_value: str) -> HoneyToken:
        """Revoke an existing token and replace it atomically.

        Args:
            old_token_value: Existing token value to revoke.
            new_token_value: Unique value for the replacement token.

        Returns:
            The persisted replacement honey token.

        Raises:
            ValidationError: If either token value is blank.
            HoneyTokenNotFoundError: If the old token does not exist.
            DuplicateHoneyTokenError: If the new token value is already in use.
        """
        self._validate_required_fields(
            ("Old token value", old_token_value),
            ("New token value", new_token_value),
        )

        try:
            old_token = self.token_repo.get_by_token(old_token_value)
            if not old_token:
                raise HoneyTokenNotFoundError(
                    f"Token '{old_token_value}' not found"
                )

            existing_new_token = self.token_repo.get_by_token(new_token_value)
            if existing_new_token:
                raise DuplicateHoneyTokenError(
                    f"Token with value '{new_token_value}' already exists"
                )

            old_token.is_active = False
            new_token = self.token_repo.create(
                project_id=old_token.project_id,
                token_type=old_token.token_type,
                token_value=new_token_value,
                label=old_token.label,
                token_metadata=old_token.token_metadata,
            )
            self.session.commit()
            return new_token
        except Exception:
            self.session.rollback()
            raise

    def list_tokens(
        self,
        project_domain: str | None = None,
        active_only: bool = True,
    ) -> list[HoneyToken]:
        """List honey tokens with optional project and activity filters.

        Args:
            project_domain: Optional domain limiting results to one project.
            active_only: Whether to exclude revoked tokens.

        Returns:
            Honey tokens matching the requested filters.

        Raises:
            ValidationError: If a supplied project domain is blank.
            ProjectNotFoundError: If a supplied project does not exist.
        """
        project_id = None
        if project_domain is not None:
            self._validate_required_fields(("Project domain", project_domain))
            project = self.project_repo.get_by_domain(project_domain)
            if not project:
                raise ProjectNotFoundError(f"Project '{project_domain}' not found")
            project_id = project.id

        if active_only:
            return self.token_repo.list_active(project_id=project_id)

        if project_id is not None:
            return self.token_repo.list_by_project(project_id)
        return self.token_repo.list()
