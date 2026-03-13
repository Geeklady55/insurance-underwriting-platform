from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine
from .rules import calculate_risk

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insurance Underwriting Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Insurance Underwriting API is running"}


@app.post("/applications", response_model=schemas.InsuranceApplicationResponse)
def create_application(
    application: schemas.InsuranceApplicationCreate,
    db: Session = Depends(get_db),
):
    risk_score, decision, flags = calculate_risk(
        age=application.age,
        smoker=application.smoker,
        annual_income=application.annual_income,
        coverage_amount=application.coverage_amount,
    )

    db_application = models.InsuranceApplication(
        full_name=application.full_name,
        age=application.age,
        smoker=application.smoker,
        annual_income=application.annual_income,
        coverage_amount=application.coverage_amount,
        risk_score=risk_score,
        decision=decision,
        status="Completed",
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


@app.get("/applications", response_model=list[schemas.InsuranceApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(models.InsuranceApplication).all()


@app.get("/applications/{application_id}", response_model=schemas.InsuranceApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = (
        db.query(models.InsuranceApplication)
        .filter(models.InsuranceApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@app.get("/sample-decision")
def sample_decision():
    risk_score, decision, flags = calculate_risk(
        age=61,
        smoker="yes",
        annual_income=28000,
        coverage_amount=800000,
    )

    return {
        "risk_score": risk_score,
        "decision": decision,
        "flags": flags,
    }
