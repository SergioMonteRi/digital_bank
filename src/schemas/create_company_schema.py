from pydantic import BaseModel


class CreateCompanySchema(BaseModel):
    monthly_revenue: float
    company_name: str
    phone: str
    email: str
    category: str
