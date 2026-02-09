class DomainError(Exception):
    code: str = "DOMAIN_ERROR"
    message: str = "A domain error occurred"
