"""Tracking pixel generator strategy."""

import secrets
from typing import Any

from app.schemas.generation import GeneratedTokenData
from app.services.generation.base import BaseGenerator


class TrackingPixelGenerator(BaseGenerator):
    """Generates realistic invisible tracking pixel image paths."""

    def generate(self, project_domain: str, params: dict[str, Any]) -> GeneratedTokenData:
        directories = ["/pixel", "/track", "/assets/img", "/static/images", "/metrics"]
        extensions = [".png", ".gif", ".jpg", ".webp"]
        
        selected_dir = secrets.choice(directories)
        selected_ext = secrets.choice(extensions)
        
        # 16 characters of randomness for the filename
        random_filename = secrets.token_hex(8)
        
        token_value = f"{selected_dir}/{random_filename}{selected_ext}"

        return GeneratedTokenData(
            token_value=token_value,
            label="Tracking Pixel",
            metadata={
                "directory": selected_dir,
                "extension": selected_ext,
                "domain_context": project_domain
            },
        )
