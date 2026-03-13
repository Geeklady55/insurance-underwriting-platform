from sqlalchemy import Column, Float, Integer, String
from .database import Base


class InsuranceApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    smoker = Column(String, nullable=False)
    annual_income = Column(Float, nullable=False)
    coverage_amount = Column(Float, nullable=False)
    status = Column(String, default="Submitted")
    risk_score = Column(Integer, default=0)
    decision = Column(String, default="Pending")
