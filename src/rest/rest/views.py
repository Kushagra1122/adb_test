import logging
import os

from pymongo import MongoClient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .todos import TodoRepository, TodoService
from .todos.exceptions import TodoPersistenceError, TodoValidationError

logger = logging.getLogger(__name__)

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']

todo_service = TodoService(TodoRepository(db))


class TodoListView(APIView):
    """List existing todos and create new ones."""

    def get(self, request):
        try:
            todos = todo_service.list_todos()
            return Response(todos, status=status.HTTP_200_OK)
        except TodoPersistenceError as exc:
            return Response(
                {'error': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            logger.exception('Unexpected error while listing todos')
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            todo = todo_service.create_todo(request.data)
            return Response(todo, status=status.HTTP_201_CREATED)
        except TodoValidationError as exc:
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TodoPersistenceError as exc:
            return Response(
                {'error': str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            logger.exception('Unexpected error while creating todo')
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
