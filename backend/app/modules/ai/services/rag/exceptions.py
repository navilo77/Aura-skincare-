from __future__ import annotations


class RAGServiceError(Exception):
    def __init__(self, message: str = "RAG service error") -> None:
        super().__init__(message)


class ChunkValidationError(RAGServiceError):
    def __init__(self, message: str = "Chunk validation failed") -> None:
        super().__init__(message)


class EmbeddingServiceError(RAGServiceError):
    def __init__(self, message: str = "Embedding generation failed") -> None:
        super().__init__(message)


class VectorStoreError(RAGServiceError):
    def __init__(self, message: str = "Vector store operation failed") -> None:
        super().__init__(message)


class RetrievalError(RAGServiceError):
    def __init__(self, message: str = "Retrieval failed") -> None:
        super().__init__(message)


class ChunkingError(RAGServiceError):
    def __init__(self, message: str = "Chunking failed") -> None:
        super().__init__(message)
