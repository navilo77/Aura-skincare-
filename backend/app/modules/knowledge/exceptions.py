from __future__ import annotations


class KnowledgeError(Exception):
    def __init__(self, message: str = "Knowledge service error") -> None:
        super().__init__(message)


class DocumentValidationError(KnowledgeError):
    def __init__(self, message: str = "Document validation failed") -> None:
        super().__init__(message)


class DocumentNotFoundError(KnowledgeError):
    def __init__(self, message: str = "Document not found") -> None:
        super().__init__(message)


class DocumentConflictError(KnowledgeError):
    def __init__(self, message: str = "Document conflict") -> None:
        super().__init__(message)
