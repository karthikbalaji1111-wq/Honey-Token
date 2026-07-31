from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.repositories.base import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Tenant)

    def get_by_slug(self, slug: str) -> Tenant | None:
        stmt = select(Tenant).where(Tenant.slug == slug)
        return self.session.scalar(stmt)

    def slug_exists(self, slug: str) -> bool:
        stmt = select(func.count()).select_from(Tenant).where(Tenant.slug == slug)
        return (self.session.scalar(stmt) or 0) > 0

    def list_active(self) -> list[Tenant]:
        stmt = select(Tenant).where(Tenant.is_active.is_(True))
        return list(self.session.scalars(stmt).all())
