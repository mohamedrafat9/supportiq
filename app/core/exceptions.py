class ProviderError(Exception):
    """Base exception for external AI provider failures."""


class ProviderAuthenticationError(ProviderError):
    """Invalid or missing provider credentials."""


class ProviderPermissionError(ProviderError):
    """The credentials do not have the required permissions."""


class ProviderRateLimitError(ProviderError):
    """The provider rate limit has been exceeded."""


class ProviderInvalidRequestError(ProviderError):
    """The provider rejected the request parameters or input."""


class ProviderUnavailableError(ProviderError):
    """The provider is temporarily unavailable or encountered a server error."""


class ProviderTimeoutError(ProviderError):
    """The provider request timed out."""


class ProviderConnectionError(ProviderError):
    """A connection to the provider could not be established."""
