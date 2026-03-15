from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import audit_models, models, schemas
from .audit_models import AuditLog
from .auth import ALGORITHM, SECRET_KEY, create_access_token
from .database import Base, SessionLocal, engine
from .rules import calculate_risk

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insurance Underwriting Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Demo login user for portfolio/testing
fake_user = {
    "username": "admin",
    "password": "password123",
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"username": username}


@app.get("/")
def home():
    return {"message": "Insurance Underwriting API is running"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != fake_user["username"]
        or form_data.password != fake_user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/applications", response_model=schemas.InsuranceApplicationResponse)
def create_application(
    application: schemas.InsuranceApplicationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
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

    audit_entry = AuditLog(
        application_id=db_application.id,
        action="CREATE_APPLICATION",
        detail=(
            f"Application created for {db_application.full_name} "
            f"by {current_user['username']}"
        ),
    )
    db.add(audit_entry)
    db.commit()

    return db_application


@app.get("/applications", response_model=list[schemas.InsuranceApplicationResponse])
def get_applications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return db.query(models.InsuranceApplication).all()


@app.get("/applications/{application_id}", response_model=schemas.InsuranceApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    application = (
        db.query(models.InsuranceApplication)
        .filter(models.InsuranceApplication.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@app.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return db.query(AuditLog).all()


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