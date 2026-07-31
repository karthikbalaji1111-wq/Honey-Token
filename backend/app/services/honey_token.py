from __future__ import annotations
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateHoneyTokenError, HoneyTokenNotFoundError, ProjectNotFoundError, ValidationError
from app.models.enums import HoneyTokenType
from app.models.honey_token import HoneyToken
from app.repositories.honey_token import HoneyTokenRepository
from app.repositories.project import ProjectRepository
from app.services.base import BaseService


class HoneyTokenService(BaseService):
    def __init__(
        self, session: Session, token_repo: HoneyTokenRepository, project_repo: ProjectRepository
    ) -> None:
        super().__init__(session)
        self.token_repo = token_repo
        self.project_repo = project_repo

    def create_token(
        self, project_domain: str, token_type: HoneyTokenType, token_value: str, label: str | None = None, metadata: dict[str, Any] | None = None
    ) -> HoneyToken:
        if not token_value:
            raise ValidationError("Token value is required")

        project = self.project_repo.get_by_domain(project_domain)
        if not project:
            raise ProjectNotFoundError(f"Project '{project_domain}' not found")

        existing_token = self.token_repo.get_by_token(token_value)
        if existing_token:
            raise DuplicateHoneyTokenError(f"Token with value '{token_value}' already exists")

        token = self.token_repo.create(
            project_id=project.id,
            token_type=token_type,
            token_value=token_value,
            label=label,
            token_metadata=metadata,
        )
        try:
            self.session.commit()
            return token
        except Exception:
            self.session.rollback()
            raise

    def revoke_token(self, token_value: str) -> None:
        token = self.token_repo.get_by_token(token_value)
        if not token:
            raise HoneyTokenNotFoundError(f"Token '{token_value}' not found")
        
        token.is_active = False
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def rotate_token(self, old_token_value: str, new_token_value: str) -> HoneyToken:
        if not new_token_value:
            raise ValidationError("New token value is required")
            
        old_token = self.token_repo.get_by_token(old_token_value)
        if not old_token:
            raise HoneyTokenNotFoundError(f"Token '{old_token_value}' not found")
            
        existing_new_token = self.token_repo.get_by_token(new_token_value)
        if existing_new_token:
            raise DuplicateHoneyTokenError(f"Token with value '{new_token_value}' already exists")

        # Disable old token
        old_token.is_active = False
        
        # Create new token
        new_token = self.token_repo.create(
            project_id=old_token.project_id,
            token_type=old_token.token_type,
            token_value=new_token_value,
            label=old_token.label,
            token_metadata=old_token.token_metadata,
        )
        try:
            self.session.commit()
            return new_token
        except Exception:
            self.session.rollback()
            raise

    def list_tokens(self, project_domain: str | None = None, active_only: bool = True) -> list[HoneyToken]:
        project_id = None
        if project_domain:
            project = self.project_repo.get_by_domain(project_domain)
            if not project:
                raise ProjectNotFoundError(f"Project '{project_domain}' not found")
            project_id = project.id
        
        if active_only:
            return self.token_repo.list_active(project_id=project_id)
            
        if project_id:
            return self.token_repo.list_by_project(project_id)
        return self.token_repo.list()
