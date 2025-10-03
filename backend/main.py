from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import os
from dotenv import load_dotenv

from backend.database import engine, get_db, Base
from backend.models import User, Medicine, Appointment, HealthMetric, EmergencyContact
from backend.schemas import (
    UserCreate, UserResponse, Token,
    MedicineCreate, MedicineResponse, MedicineUpdate,
    AppointmentCreate, AppointmentResponse, AppointmentUpdate,
    HealthMetricCreate, HealthMetricResponse,
    EmergencyContactCreate, EmergencyContactResponse,
    SOSRequest, SMSRequest
)
from backend.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

# ADDED: Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedPal API",
    version="2.0.0",
    description="Healthcare Management System API"
)

# ADDED: CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== HEALTH CHECK ====================
@app.get("/")
def read_root():
    return {
        "message": "Welcome to MedPal API",
        "status": "active",
        "version": "2.0.0"
    }

@app.get("/health")
def health_check():
    """ADDED: Health check endpoint"""
    twilio_configured = all([
        os.environ.get("TWILIO_ACCOUNT_SID"),
        os.environ.get("TWILIO_AUTH_TOKEN"),
        os.environ.get("TWILIO_PHONE_NUMBER")
    ])
    
    return {
        "status": "healthy",
        "database": "connected",
        "twilio_configured": twilio_configured
    }
@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint works!"}

# ==================== AUTHENTICATION ====================
@app.post("/api/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and receive access token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# ==================== MEDICINES ====================
@app.post("/api/medicines", response_model=MedicineResponse, status_code=201)
def add_medicine(
    medicine: MedicineCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new medicine"""
    new_medicine = Medicine(**medicine.dict(), user_id=current_user.id)
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine

@app.get("/api/medicines", response_model=List[MedicineResponse])
def get_medicines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all medicines for current user"""
    return db.query(Medicine).filter(Medicine.user_id == current_user.id).all()

@app.put("/api/medicines/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    medicine_update: MedicineUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ADDED: Update a medicine"""
    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id,
        Medicine.user_id == current_user.id
    ).first()
    
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Update fields
    for field, value in medicine_update.dict(exclude_unset=True).items():
        setattr(medicine, field, value)
    
    db.commit()
    db.refresh(medicine)
    return medicine

@app.delete("/api/medicines/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a medicine"""
    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id,
        Medicine.user_id == current_user.id
    ).first()
    
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    db.delete(medicine)
    db.commit()
    return {"message": "Medicine deleted successfully"}

# ==================== APPOINTMENTS ====================
@app.post("/api/appointments", response_model=AppointmentResponse, status_code=201)
def add_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new appointment"""
    new_appointment = Appointment(**appointment.dict(), user_id=current_user.id)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@app.get("/api/appointments", response_model=List[AppointmentResponse])
def get_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all appointments for current user"""
    return db.query(Appointment).filter(Appointment.user_id == current_user.id).all()

@app.put("/api/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ADDED: Update an appointment"""
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    for field, value in appointment_update.dict(exclude_unset=True).items():
        setattr(appointment, field, value)
    
    db.commit()
    db.refresh(appointment)
    return appointment

@app.delete("/api/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an appointment"""
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}

# ==================== HEALTH METRICS ====================
@app.post("/api/health_metrics", response_model=HealthMetricResponse, status_code=201)
def add_health_metric(
    metric: HealthMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new health metric"""
    new_metric = HealthMetric(**metric.dict(), user_id=current_user.id)
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

@app.get("/api/health_metrics", response_model=List[HealthMetricResponse])
def get_health_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all health metrics for current user"""
    return db.query(HealthMetric).filter(HealthMetric.user_id == current_user.id).all()

# ==================== EMERGENCY CONTACTS ====================
@app.post("/api/emergency_contacts", response_model=EmergencyContactResponse, status_code=201)
def add_emergency_contact(
    contact: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new emergency contact"""
    new_contact = EmergencyContact(**contact.dict(), user_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@app.get("/api/emergency_contacts", response_model=List[EmergencyContactResponse])
def get_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all emergency contacts for current user"""
    return db.query(EmergencyContact).filter(EmergencyContact.user_id == current_user.id).all()

# ==================== TWILIO / SMS ====================
def get_twilio_client():
    """ADDED: Get Twilio client with proper error handling"""
    from twilio.rest import Client
    
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    
    if not account_sid or not auth_token:
        return None
    
    try:
        return Client(account_sid, auth_token)
    except Exception:
        return None

@app.post("/api/send-sms")
def send_sms(
    sms_request: SMSRequest,
    current_user: User = Depends(get_current_user)
):
    """ADDED: Send SMS via Twilio"""
    from_phone = os.environ.get("TWILIO_PHONE_NUMBER")
    client = get_twilio_client()
    
    # Simulation mode if Twilio not configured
    if not client or not from_phone:
        return {
            "message": "SMS sent (simulation mode)",
            "simulation": True,
            "to": sms_request.to,
            "body": sms_request.message
        }
    
    try:
        message = client.messages.create(
            body=sms_request.message,
            from_=from_phone,
            to=sms_request.to
        )
        return {
            "message": "SMS sent successfully",
            "sid": message.sid,
            "status": message.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")

@app.post("/api/sos")
def send_sos(
    sos: SOSRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send emergency SOS to all emergency contacts"""
    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id
    ).all()
    
    if not contacts:
        raise HTTPException(status_code=400, detail="No emergency contacts found")
    
    client = get_twilio_client()
    from_phone = os.environ.get("TWILIO_PHONE_NUMBER")
    
    # Simulation mode if Twilio not configured
    if not client or not from_phone:
        return {
            "message": "SOS sent (simulation mode)",
            "simulation": True,
            "sent_to": [c.name for c in contacts],
            "contacts_notified": len(contacts)
        }
    
    # Send real SMS
    sent_to = []
    failed = []
    
    for contact in contacts:
        try:
            message = client.messages.create(
                body=f"🚨 EMERGENCY ALERT from {current_user.full_name}: {sos.message}",
                from_=from_phone,
                to=contact.phone
            )
            sent_to.append(contact.name)
        except Exception as e:
            failed.append({"contact": contact.name, "error": str(e)})
    
    return {
        "message": "SOS sent successfully",
        "sent_to": sent_to,
        "contacts_notified": len(sent_to),
        "failed": failed if failed else None
    }

# ==================== ERROR HANDLERS ====================
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "detail": str(exc)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)