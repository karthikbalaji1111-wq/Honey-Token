from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateDomainError, ProjectNotFoundError, TenantNotFoundError, ValidationError
from app.models.project import Project
from app.repositories.project import ProjectRepository
from app.repositories.tenant import TenantRepository
from app.services.base import BaseService


class ProjectService(BaseService):
    def __init__(
        self, session: Session, project_repo: ProjectRepository, tenant_repo: TenantRepository
    ) -> None:
        super().__init__(session)
        self.project_repo = project_repo
        self.tenant_repo = tenant_repo

    def create_project(self, tenant_slug: str, name: str, domain: str) -> Project:
        if not name or not domain:
            raise ValidationError("Name and domain are required")

        tenant = self.tenant_repo.get_by_slug(tenant_slug)
        if not tenant:
            raise TenantNotFoundError(f"Tenant '{tenant_slug}' not found")

        existing_project = self.project_repo.get_by_domain(domain)
        if existing_project:
            raise DuplicateDomainError(f"Project with domain '{domain}' already exists")

        project = self.project_repo.create(tenant_id=tenant.id, name=name, domain=domain)
        try:
            self.session.commit()
            return project
        except Exception:
            self.session.rollback()
            raise

    def get_project(self, domain: str) -> Project:
        project = self.project_repo.get_by_domain(domain)
        if not project:
            raise ProjectNotFoundError(f"Project for domain '{domain}' not found")
        return project

    def list_projects(self, tenant_slug: str | None = None, active_only: bool = True) -> list[Project]:
        tenant_id = None
        if tenant_slug:
            tenant = self.tenant_repo.get_by_slug(tenant_slug)
            if not tenant:
                raise TenantNotFoundError(f"Tenant '{tenant_slug}' not found")
            tenant_id = tenant.id
        
        if active_only:
            return self.project_repo.list_active(tenant_id=tenant_id)
        
        if tenant_id:
            return self.project_repo.list_by_tenant(tenant_id)
        return self.project_repo.list()

    def delete_project(self, domain: str) -> None:
        project = self.project_repo.get_by_domain(domain)
        if not project:
            raise ProjectNotFoundError(f"Project for domain '{domain}' not found")
        
        self.project_repo.delete(project.id)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
