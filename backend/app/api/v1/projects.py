"""Version 1 project API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.api.dependencies import get_project_service
from app.schemas.error import ErrorResponse
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
    description="Creates a project for an existing tenant.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Owning tenant does not exist.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Project domain already exists.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Request or domain validation failed.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Unexpected server error.",
        },
    },
)
def create_project(
    payload: ProjectCreate,
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    """Create and serialize a project."""
    return service.create_project(
        tenant_slug=payload.tenant_slug,
        name=payload.name,
        domain=payload.domain,
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="List projects",
    description="Lists projects with optional tenant and activity filters.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Supplied tenant does not exist.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Request or domain validation failed.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Unexpected server error.",
        },
    },
)
def list_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    tenant_slug: Annotated[
        str | None,
        Query(
            max_length=100,
            description="Optional tenant slug used to scope results.",
        ),
    ] = None,
    active_only: Annotated[
        bool,
        Query(description="Whether to exclude inactive projects."),
    ] = True,
) -> list[ProjectResponse]:
    """List and serialize projects."""
    return service.list_projects(
        tenant_slug=tenant_slug,
        active_only=active_only,
    )


@router.get(
    "/{domain}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a project",
    description="Retrieves one project by its domain.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Project does not exist.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Request or domain validation failed.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Unexpected server error.",
        },
    },
)
def get_project(
    domain: Annotated[
        str,
        Path(
            min_length=1,
            max_length=253,
            description="Project domain identifier.",
        ),
    ],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    """Retrieve and serialize a project."""
    return service.get_project(domain=domain)


@router.delete(
    "/{domain}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Deletes a project through the project service.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Project does not exist.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Request or domain validation failed.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Unexpected server error.",
        },
    },
)
def delete_project(
    domain: Annotated[
        str,
        Path(
            min_length=1,
            max_length=253,
            description="Project domain identifier.",
        ),
    ],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    """Delete a project."""
    service.delete_project(domain=domain)
