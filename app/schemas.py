from pydantic import BaseModel, Field


class InsuranceApplicationCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100)
    smoker: str = Field(..., pattern="^(yes|no|Yes|No)$")
    annual_income: float = Field(..., gt=0)
    coverage_amount: float = Field(..., gt=0)


class InsuranceApplicationResponse(BaseModel):
    id: int
    full_name: str
    age: int
    smoker: str
    annual_income: float
    coverage_amount: float
    status: str
    risk_score: int
    decision: str

    class Config:
        from_attributes = True
