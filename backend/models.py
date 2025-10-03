from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    medicines = relationship("Medicine", back_populates="owner")
    appointments = relationship("Appointment", back_populates="owner")
    health_metrics = relationship("HealthMetric", back_populates="owner")
    emergency_contacts = relationship("EmergencyContact", back_populates="owner")

class Medicine(Base):
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    dosage = Column(String)
    frequency = Column(String)
    time_of_day = Column(String)
    start_date = Column(String)
    end_date = Column(String, nullable=True)
    prescriber = Column(String)
    notes = Column(Text, nullable=True)
    status = Column(String, default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="medicines")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor = Column(String)
    specialty = Column(String, nullable=True)
    date = Column(String)
    time = Column(String)
    location = Column(String)
    reason = Column(Text)
    notes = Column(Text, nullable=True)
    reminder_enabled = Column(Boolean, default=True)
    status = Column(String, default="Scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="appointments")

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    metric_type = Column(String)
    value = Column(Float)
    unit = Column(String)
    measured_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    source = Column(String, default="Manual")
    
    owner = relationship("User", back_populates="health_metrics")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    contact_relationship = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="emergency_contacts")
