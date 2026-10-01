class TodoError(Exception):
    """Base exception for todo-related failures."""


class TodoValidationError(TodoError):
    """Raised when incoming todo data fails validation."""


class TodoPersistenceError(TodoError):
    """Raised when a MongoDB read/write operation fails."""
