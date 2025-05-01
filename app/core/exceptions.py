from fastapi import HTTPException
from typing import Any

class NotFoundException(HTTPException):
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(
            status_code=404,
            detail=f"{entity} with id {entity_id} not found"
        )

class DatabaseException(HTTPException):
    def __init__(self, operation: str, detail: str = None):
        super().__init__(
            status_code=500,
            detail=f"Database error during {operation}: {detail or 'unknown error'}"
        ) 