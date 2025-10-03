"""
Pydantic schemas for MedPal API
Fixed for Pydantic V2 compatibility
"""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# ==================== USER SCHEMAS ====================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # FIXED: Pydantic V2 syntax


class Token(BaseModel):
    access_token: str
    token_type: str


# ==================== MEDICINE SCHEMAS ====================

class MedicineCreate(BaseModel):
    name: str
    dosage: str
    frequency: str
    time_of_day: Optional[str] = None
    next_dose_time: Optional[str] = None
    prescriber: Optional[str] = None
    status: str = "Active"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None


class MedicineUpdate(BaseModel):
    """Schema for updating medicines"""
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    time_of_day: Optional[str] = None
    next_dose_time: Optional[str] = None
    prescriber: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None


class MedicineResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str
    time_of_day: Optional[str] = None
    next_dose_time: Optional[str] = None
    prescriber: Optional[str] = None
    status: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    notes: Optional[str] = None
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # FIXED: Pydantic V2 syntax


# ==================== APPOINTMENT SCHEMAS ====================

class AppointmentCreate(BaseModel):
    doctor: str
    specialty: Optional[str] = None
    date: str
    time: str
    location: Optional[str] = None
    reason: Optional[str] = None
    contact: Optional[str] = None
    insurance: Optional[str] = None
    notes: Optional[str] = None
    reminder_enabled: bool = True
    status: str = "Scheduled"


class AppointmentUpdate(BaseModel):
    """Schema for updating appointments"""
    doctor: Optional[str] = None
    specialty: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    reason: Optional[str] = None
    contact: Optional[str] = None
    insurance: Optional[str] = None
    notes: Optional[str] = None
    reminder_enabled: Optional[bool] = None
    status: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    doctor: str
    specialty: Optional[str] = None
    date: str
    time: str
    location: Optional[str] = None
    reason: Optional[str] = None
    contact: Optional[str] = None
    insurance: Optional[str] = None
    notes: Optional[str] = None
    reminder_enabled: bool
    status: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # FIXED: Pydantic V2 syntax


# ==================== HEALTH METRIC SCHEMAS ====================

class HealthMetricCreate(BaseModel):
    metric_type: str  # e.g., "blood_pressure", "glucose", "weight"
    value: float
    unit: str
    notes: Optional[str] = None
    source: str = "Manual"


class HealthMetricResponse(BaseModel):
    id: int
    metric_type: str
    value: float
    unit: str
    measured_at: datetime
    notes: Optional[str] = None
    source: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)  # FIXED: Pydantic V2 syntax


# ==================== EMERGENCY CONTACT SCHEMAS ====================

class EmergencyContactCreate(BaseModel):
    name: str
    contact_relationship: str
    phone: str
    email: Optional[str] = None
    is_primary: bool = False
    is_medical: bool = False
    address: Optional[str] = None
    notes: Optional[str] = None


class EmergencyContactResponse(BaseModel):
    id: int
    name: str
    contact_relationship: str
    phone: str
    email: Optional[str] = None
    is_primary: bool
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # FIXED: Pydantic V2 syntax


# ==================== SOS / SMS SCHEMAS ====================

class SOSRequest(BaseModel):
    message: Optional[str] = "Emergency! I need help."


class SMSRequest(BaseModel):
    """Schema for sending SMS"""
    to: str
    message: str