from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateTenantError, TenantNotFoundError, ValidationError
from app.models.tenant import Tenant
from app.repositories.tenant import TenantRepository
from app.services.base import BaseService


class TenantService(BaseService):
    def __init__(self, session: Session, tenant_repo: TenantRepository) -> None:
        super().__init__(session)
        self.tenant_repo = tenant_repo

    def create_tenant(self, name: str, slug: str) -> Tenant:
        if not name or not slug:
            raise ValidationError("Name and slug are required")

        if self.tenant_repo.slug_exists(slug):
            raise DuplicateTenantError(f"Tenant with slug '{slug}' already exists")

        tenant = self.tenant_repo.create(name=name, slug=slug)
        try:
            self.session.commit()
            return tenant
        except Exception:
            self.session.rollback()
            raise

    def get_tenant(self, slug: str) -> Tenant:
        tenant = self.tenant_repo.get_by_slug(slug)
        if not tenant:
            raise TenantNotFoundError(f"Tenant '{slug}' not found")
        return tenant

    def list_tenants(self, active_only: bool = True) -> list[Tenant]:
        if active_only:
            return self.tenant_repo.list_active()
        return self.tenant_repo.list()

    def delete_tenant(self, slug: str) -> None:
        tenant = self.tenant_repo.get_by_slug(slug)
        if not tenant:
            raise TenantNotFoundError(f"Tenant '{slug}' not found")
        
        self.tenant_repo.delete(tenant.id)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
