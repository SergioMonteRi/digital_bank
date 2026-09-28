from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class IndividualTable(Base):
    __tablename__ = "individual"

    id: Mapped[int] = mapped_column(primary_key=True)
    monthly_income: Mapped[float]
    age: Mapped[int]
    full_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    category: Mapped[str]
    balance: Mapped[float]
