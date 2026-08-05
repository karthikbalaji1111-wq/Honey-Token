"""Static registry for token generators."""

from typing import Mapping

from app.models.enums import HoneyTokenType
from app.services.generation.api_key import ApiKeyGenerator
from app.services.generation.base import BaseGenerator
from app.services.generation.hidden_url import HiddenUrlGenerator
from app.services.generation.tracking_pixel import TrackingPixelGenerator

# Map Token Type to an instantiated generator strategy.
GENERATOR_REGISTRY: Mapping[HoneyTokenType, BaseGenerator] = {
    HoneyTokenType.API_KEY: ApiKeyGenerator(),
    HoneyTokenType.URL: HiddenUrlGenerator(),
    HoneyTokenType.PIXEL: TrackingPixelGenerator(),
}
