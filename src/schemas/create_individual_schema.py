from pydantic import BaseModel


class CreateIndividualSchema(BaseModel):
    monthly_income: float
    age: int
    full_name: str
    phone: str
    email: str
    category: str
