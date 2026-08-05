"""Hidden URL generator strategy."""

import secrets
from typing import Any

from app.schemas.generation import GeneratedTokenData
from app.services.generation.base import BaseGenerator


class HiddenUrlGenerator(BaseGenerator):
    """Generates realistic hidden administration and configuration paths."""

    def generate(self, project_domain: str, params: dict[str, Any]) -> GeneratedTokenData:
        paths = [
            "/admin/login",
            "/.git/config",
            "/private/api",
            "/internal/dashboard",
            "/config",
            "/wp-admin/admin-ajax.php",
            "/.env",
            "/api/v1/internal/users",
        ]
        
        selected_path = secrets.choice(paths)
        
        # Add random token or query parameters to make it unique per generation
        random_suffix = secrets.token_hex(8)
        
        # Decide if we append a query param or unique suffix based on path type
        if ".git" in selected_path or ".env" in selected_path:
            # For strict files, we might prepend a unique directory
            token_value = f"/backup-{random_suffix}{selected_path}"
        else:
            token_value = f"{selected_path}?auth_token={random_suffix}"

        return GeneratedTokenData(
            token_value=token_value,
            label=f"Hidden Path: {selected_path}",
            metadata={"base_path": selected_path, "domain_context": project_domain},
        )
