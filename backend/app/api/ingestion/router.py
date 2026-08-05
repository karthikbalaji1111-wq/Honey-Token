"""Public ingestion API routes."""

from typing import Annotated

from fastapi import APIRouter, Path, Request, Response, status

router = APIRouter(tags=["ingestion"])

# 1x1 transparent GIF (43 bytes)
_TRANSPARENT_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00"
    b"\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21"
    b"\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00"
    b"\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44"
    b"\x01\x00\x3b"
)


@router.get(
    "/t/{token_value}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Trigger a URL honey token",
    description="Public ingestion endpoint for URL and link honey tokens.",
    response_class=Response,
)
def trigger_url_token(
    token_value: Annotated[
        str,
        Path(description="Honey-token value embedded in the URL."),
    ],
) -> Response:
    """Accept a URL honey-token trigger."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/px/{token_value}.gif",
    summary="Trigger a tracking pixel honey token",
    description="Public ingestion endpoint for tracking pixel honey tokens.",
    response_class=Response,
)
def trigger_pixel_token(
    token_value: Annotated[
        str,
        Path(description="Honey-token value embedded in the pixel URL."),
    ],
) -> Response:
    """Accept a tracking-pixel honey-token trigger and return a transparent GIF."""
    return Response(
        content=_TRANSPARENT_GIF,
        media_type="image/gif",
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/collect/{token_value}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Collect a programmable honey token trigger",
    description="Public ingestion endpoint for API key and programmable honey tokens.",
    response_class=Response,
)
def collect_token(
    token_value: Annotated[
        str,
        Path(description="Honey-token value embedded in the collection URL."),
    ],
    request: Request,
) -> Response:
    """Accept a programmable honey-token trigger."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)
