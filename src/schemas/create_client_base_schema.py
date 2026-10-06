from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.helpers.regex_patterns import PHONE_PATTERN


class CreateClientBaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        str_min_length=1,
        str_max_length=255,
    )

    phone: str = Field(pattern=PHONE_PATTERN)
    email: EmailStr
