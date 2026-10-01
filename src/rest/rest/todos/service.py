from .exceptions import TodoValidationError
from .repository import TodoRepository


class TodoService:
    """Business logic for creating and listing todos."""

    MAX_DESCRIPTION_LENGTH = 500

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def list_todos(self):
        return self._repository.list_all()

    def create_todo(self, payload):
        description = self._extract_description(payload)
        return self._repository.create(description)

    def _extract_description(self, payload):
        if not isinstance(payload, dict):
            raise TodoValidationError('Request body must be a JSON object')

        description = payload.get('description')
        if description is None:
            raise TodoValidationError('Field "description" is required')

        if not isinstance(description, str):
            raise TodoValidationError('Field "description" must be a string')

        description = description.strip()
        if not description:
            raise TodoValidationError('Field "description" cannot be empty')

        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise TodoValidationError(
                f'Field "description" must be at most '
                f'{self.MAX_DESCRIPTION_LENGTH} characters'
            )

        return description
