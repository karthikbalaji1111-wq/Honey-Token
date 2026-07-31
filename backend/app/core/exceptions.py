class HoneyShieldError(Exception):
    """Base exception for all HoneyShield domain errors."""
    pass

class ValidationError(HoneyShieldError):
    pass

class BusinessRuleViolationError(HoneyShieldError):
    pass

class TenantNotFoundError(HoneyShieldError):
    pass

class ProjectNotFoundError(HoneyShieldError):
    pass

class HoneyTokenNotFoundError(HoneyShieldError):
    pass

class DetectionEventNotFoundError(HoneyShieldError):
    pass

class DuplicateTenantError(HoneyShieldError):
    pass

class DuplicateDomainError(HoneyShieldError):
    pass

class DuplicateHoneyTokenError(HoneyShieldError):
    pass
