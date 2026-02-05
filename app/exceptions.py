"""Custom exceptions for the application."""


class FastpaymentException(Exception):
    """Base exception for Fastpayment application."""

    pass


class NotFoundError(FastpaymentException):
    """Raised when a resource is not found."""

    pass


class AuthenticationError(FastpaymentException):
    """Raised when authentication fails."""

    pass


class AuthorizationError(FastpaymentException):
    """Raised when authorization fails."""

    pass
