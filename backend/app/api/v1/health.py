from fastapi import APIRouter

router = APIRouter(tags=["health"])


def health_payload() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/health")
def health_check() -> dict[str, str]:
    return health_payload()
