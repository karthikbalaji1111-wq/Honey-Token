from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Project)

    def get_by_domain(self, domain: str) -> Project | None:
        stmt = select(Project).where(
            Project.domain == domain,
        )
        return self.session.scalar(stmt)

    def list_by_tenant(self, tenant_id: int) -> list[Project]:
        stmt = select(Project).where(Project.tenant_id == tenant_id)
        return list(self.session.scalars(stmt).all())

    def list_active(self, tenant_id: int | None = None) -> list[Project]:
        stmt = select(Project).where(Project.is_active.is_(True))
        if tenant_id is not None:
            stmt = stmt.where(Project.tenant_id == tenant_id)
        return list(self.session.scalars(stmt).all())
