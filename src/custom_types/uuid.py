from uuid import UUID

from sqlalchemy import String
from sqlalchemy.types import TypeDecorator


class UUIDType(TypeDecorator):  # pylint: disable=too-many-ancestors
    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if not isinstance(value, UUID):
            value = UUID(str(value))

        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        return UUID(value)

    def process_literal_param(self, value, dialect):
        return value
