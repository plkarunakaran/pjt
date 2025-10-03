"""
MedPal Helper Functions
Provides utility functions for the Streamlit application
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Import DataManager
try:
    from utils.data_manager import DataManager
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils.data_manager import DataManager


# ============================================
# SESSION STATE MANAGEMENT
# ============================================

def init_session_state():
    """Initialize Streamlit session state with persistent data."""
    data_manager = DataManager()

    defaults = {
        "medicines": data_manager.load_medicines(),
        "appointments": data_manager.load_appointments(),
        "health_metrics": data_manager.load_health_metrics(),
        "family_members": data_manager.load_family_members(),
        "emergency_contacts": data_manager.load_emergency_contacts(),
        "medical_profile": data_manager.load_medical_profile(),
        "user_preferences": data_manager.load_user_preferences(),
        "emergency_logs": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "app_initialized" not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================
# MEDICINE FUNCTIONS
# ============================================

def get_active_medicines() -> List[Dict]:
    """Get list of active medicines"""
    return [m for m in st.session_state.get("medicines", []) if m.get("status") == "Active"]


def get_next_medicine_dose(medicine: Dict) -> Optional[datetime]:
    """Calculate next dose datetime based on frequency."""
    try:
        next_dose_time = medicine.get("next_dose_time", "08:00")
        frequency = medicine.get("frequency", "").lower()

        today = datetime.now().date()
        next_dose_datetime = datetime.strptime(f"{today} {next_dose_time}", "%Y-%m-%d %H:%M")

        # If time has passed, calculate next dose based on frequency
        if next_dose_datetime < datetime.now():
            if "once" in frequency:
                next_dose_datetime += timedelta(days=1)
            elif "twice" in frequency:
                next_dose_datetime += timedelta(hours=12)
            elif "three" in frequency or "thrice" in frequency:
                next_dose_datetime += timedelta(hours=8)
            elif "four" in frequency:
                next_dose_datetime += timedelta(hours=6)
            else:
                next_dose_datetime += timedelta(days=1)

        return next_dose_datetime
    except Exception as e:
        print(f"Error calculating next dose: {e}")
        return None
def format_time_until(timedelta_obj: timedelta) -> str:
    """
    Format timedelta into human-readable string.
    """
    try:
        total_seconds = int(timedelta_obj.total_seconds())
        
        # Handle negative (overdue)
        if total_seconds < 0:
            total_seconds = abs(total_seconds)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            
            if hours > 0:
                return f"{hours}h {minutes}m ago"
            elif minutes > 0:
                return f"{minutes}m ago"
            else:
                return "Just now"
        
        # Handle positive (upcoming)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return "Now"
    except Exception as e:
        print(f"Error formatting time: {e}")
        return "Unknown"


def get_medicine_reminders() -> List[Dict]:
    """Return reminders for medicines with urgency levels."""
    reminders = []
    now = datetime.now()

    for med in get_active_medicines():
        next_dose = get_next_medicine_dose(med)
        if not next_dose:
            continue

        diff = next_dose - now
        hours = diff.total_seconds() / 3600

        # Determine urgency level
        if hours < 0:
            urgency = "overdue"
        elif hours <= 0.5:
            urgency = "urgent"
        elif hours <= 2:
            urgency = "soon"
        elif hours <= 6:
            urgency = "upcoming"
        else:
            urgency = "scheduled"

        reminders.append({
            "medicine": med,
            "next_dose": next_dose,
            "time_until": diff,
            "hours_until": hours,
            "urgency": urgency
        })

    # Sort by urgency and time
    urgency_order = {"overdue": 0, "urgent": 1, "soon": 2, "upcoming": 3, "scheduled": 4}
    reminders.sort(key=lambda r: (urgency_order.get(r["urgency"], 5), r["time_until"]))
    return reminders


def get_urgent_reminders() -> List[Dict]:
    """Get only urgent, overdue, and soon reminders"""
    return [r for r in get_medicine_reminders() if r["urgency"] in ["overdue", "urgent", "soon"]]


def get_reminders_today() -> List[Dict]:
    """Get all medicine reminders for today."""
    today = datetime.now().date()
    return [r for r in get_medicine_reminders() if r["next_dose"].date() == today]


# ============================================
# TIME FORMATTING
# ============================================

def format_time_until(timedelta_obj: timedelta) -> str:
    """
    Format timedelta into human-readable string.
    FIXED: This function was missing!
    """
    try:
        total_seconds = int(timedelta_obj.total_seconds())
        
        # Handle negative (overdue)
        if total_seconds < 0:
            total_seconds = abs(total_seconds)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            
            if hours > 0:
                return f"{hours}h {minutes}m ago"
            elif minutes > 0:
                return f"{minutes}m ago"
            else:
                return "Just now"
        
        # Handle positive (upcoming)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return "Now"
    except Exception as e:
        print(f"Error formatting time: {e}")
        return "Unknown"


def format_date(date_str: str, style: str = "readable") -> str:
    """Format date string for display"""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if style == "readable":
            return d.strftime("%B %d, %Y")
        elif style == "short":
            return d.strftime("%m/%d/%Y")
        return d.strftime("%Y-%m-%d")
    except Exception:
        return date_str


def format_time(time_str: str, style: str = "12h") -> str:
    """Format time string for display"""
    try:
        t = datetime.strptime(time_str, "%H:%M").time()
        return t.strftime("%I:%M %p") if style == "12h" else t.strftime("%H:%M")
    except Exception:
        return time_str


def time_until(target_datetime: datetime) -> str:
    """Calculate time until target datetime in human-readable format"""
    try:
        if isinstance(target_datetime, str):
            target_datetime = datetime.strptime(target_datetime, "%Y-%m-%d %H:%M:%S")
        
        now = datetime.now()
        diff = target_datetime - now
        
        if diff.total_seconds() < 0:
            return "Past due"
        
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days} day(s), {hours} hour(s)"
        elif hours > 0:
            return f"{hours} hour(s), {minutes} minute(s)"
        else:
            return f"{minutes} minute(s)"
    except Exception:
        return "Unknown"


# ============================================
# APPOINTMENT FUNCTIONS
# ============================================

def get_upcoming_appointments(days_ahead: int = 30) -> List[Dict]:
    """Get upcoming appointments within specified days"""
    appointments = st.session_state.get("appointments", [])
    now = datetime.now().date()
    limit = now + timedelta(days=days_ahead)

    upcoming = []
    for appt in appointments:
        try:
            appt_date = datetime.strptime(appt.get("date", ""), "%Y-%m-%d").date()
            if now <= appt_date <= limit:
                upcoming.append(appt)
        except ValueError:
            continue

    return sorted(upcoming, key=lambda x: x.get("date", ""))


# ============================================
# HEALTH METRICS
# ============================================

def get_recent_health_metrics(days_back: int = 30, metric_type: Optional[str] = None) -> List[Dict]:
    """Get recent health metrics, optionally filtered by type"""
    metrics = st.session_state.get("health_metrics", [])
    past = datetime.now().date() - timedelta(days=days_back)

    recent = []
    for m in metrics:
        try:
            d = datetime.strptime(m.get("date", ""), "%Y-%m-%d").date()
            if d >= past and (metric_type is None or m.get("type") == metric_type):
                recent.append(m)
        except ValueError:
            continue

    return sorted(recent, key=lambda m: (m.get("date", ""), m.get("time", "")), reverse=True)


def calculate_bmi(weight_kg: float, height_cm: float) -> Optional[float]:
    """Calculate BMI from weight and height"""
    try:
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 1)
    except Exception:
        return None


def get_bmi_category(bmi: Optional[float]) -> str:
    """Get BMI category"""
    if bmi is None:
        return "Unknown"
    elif bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


# ============================================
# EMERGENCY FUNCTIONS
# ============================================

def get_emergency_info() -> Dict:
    """Get critical emergency information"""
    profile = st.session_state.get("medical_profile", {})
    contacts = st.session_state.get("emergency_contacts", [])
    active_meds = get_active_medicines()

    primary_contact = next((c for c in contacts if c.get("is_primary")), None)

    return {
        "medical_profile": profile,
        "primary_contact": primary_contact,
        "emergency_contacts": contacts,
        "active_medicines": active_meds,
    }


# ============================================
# VALIDATION FUNCTIONS
# ============================================

def validate_phone(phone: str) -> bool:
    """Validate phone number"""
    if not phone:
        return False
    digits = "".join(c for c in str(phone) if c.isdigit())
    return 7 <= len(digits) <= 15


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    return "@" in str(email) and "." in str(email).split("@")[-1]


# ============================================
# DATA PERSISTENCE
# ============================================

def sync_data():
    """Synchronize session state data with persistent storage"""
    dm = DataManager()
    
    if "medicines" in st.session_state:
        dm.save_medicines(st.session_state.medicines)
    if "appointments" in st.session_state:
        dm.save_appointments(st.session_state.appointments)
    if "health_metrics" in st.session_state:
        dm.save_health_metrics(st.session_state.health_metrics)
    if "family_members" in st.session_state:
        dm.save_family_members(st.session_state.family_members)
    if "emergency_contacts" in st.session_state:
        dm.save_emergency_contacts(st.session_state.emergency_contacts)
    if "medical_profile" in st.session_state:
        dm.save_medical_profile(st.session_state.medical_profile)
    if "user_preferences" in st.session_state:
        dm.save_user_preferences(st.session_state.user_preferences)

    st.session_state.last_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clear_session_data():
    """Clear all session state data"""
    keys_to_clear = [
        "medicines", "appointments", "health_metrics", "family_members",
        "emergency_contacts", "medical_profile", "user_preferences", "emergency_logs"
    ]
    
    for key in keys_to_clear:
        st.session_state.pop(key, None)
    
    init_session_state()


# ============================================
# UTILITY FUNCTIONS
# ============================================

def calculate_age(birth_date_str: str) -> Optional[int]:
    """Calculate age from birth date"""
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    except Exception:
        return None


def format_medicine_frequency(frequency: str) -> str:
    """Format medicine frequency for display"""
    frequency_map = {
        'once daily': 'Once per day',
        'twice daily': 'Twice per day',
        'three times daily': '3 times per day',
        'four times daily': '4 times per day',
        'as needed': 'As needed',
        'every other day': 'Every other day',
        'weekly': 'Once per week'
    }
    
    return frequency_map.get(frequency.lower(), frequency.title())


def get_dashboard_summary() -> Dict:
    """Get summary statistics for dashboard"""
    medicines = st.session_state.get("medicines", [])
    appointments = st.session_state.get("appointments", [])
    health_metrics = st.session_state.get("health_metrics", [])
    family_members = st.session_state.get("family_members", [])
    
    active_medicines = len([m for m in medicines if m.get("status") == "Active"])
    upcoming_appointments = len(get_upcoming_appointments(30))
    health_records = len(health_metrics)
    family_count = len(family_members)
    
    return {
        "active_medicines": active_medicines,
        "upcoming_appointments": upcoming_appointments,
        "health_records": health_records,
        "family_members": family_count
    }