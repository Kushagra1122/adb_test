import logging
from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from .exceptions import TodoPersistenceError

logger = logging.getLogger(__name__)


class TodoRepository:
    """Data-access layer for todo documents stored in MongoDB."""

    COLLECTION_NAME = 'todos'

    def __init__(self, db):
        self._collection: Collection = db[self.COLLECTION_NAME]

    def list_all(self):
        try:
            cursor = self._collection.find().sort('created_at', -1)
            return [self._serialize(document) for document in cursor]
        except PyMongoError as exc:
            logger.exception('Failed to fetch todos from MongoDB')
            raise TodoPersistenceError('Unable to fetch todos') from exc

    def create(self, description):
        document = {
            'description': description,
            'created_at': datetime.utcnow(),
        }
        try:
            result = self._collection.insert_one(document)
            document['_id'] = result.inserted_id
            return self._serialize(document)
        except PyMongoError as exc:
            logger.exception('Failed to insert todo into MongoDB')
            raise TodoPersistenceError('Unable to create todo') from exc

    def get_by_id(self, todo_id):
        try:
            document = self._collection.find_one({'_id': ObjectId(todo_id)})
        except (InvalidId, PyMongoError) as exc:
            logger.exception('Failed to fetch todo %s', todo_id)
            raise TodoPersistenceError('Unable to fetch todo') from exc

        return self._serialize(document) if document else None

    @staticmethod
    def _serialize(document):
        return {
            'id': str(document['_id']),
            'description': document['description'],
            'created_at': document.get('created_at').isoformat() + 'Z'
            if document.get('created_at') else None,
        }
