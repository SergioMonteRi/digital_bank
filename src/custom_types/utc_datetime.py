from datetime import timezone

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


class UTCDateTime(TypeDecorator):  # pylint: disable=too-many-ancestors
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if value.tzinfo is None:
            raise ValueError(
                f"UTCDateTime requires an aware datetime, got a naive one: {value!r}"
            )

        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        return value.replace(tzinfo=timezone.utc)

    def process_literal_param(self, value, dialect):
        return value
