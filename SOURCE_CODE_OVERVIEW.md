# MedPal - Complete Source Code Overview

## Application Summary

MedPal is a comprehensive health management application built with **Python 3.11+** and **Streamlit**. It provides complete health tracking functionality including medicine management, appointments, health metrics, family health profiles, and emergency information.

## Technology Stack

- **Framework**: Streamlit 1.28+
- **Data Processing**: Pandas 2.0+
- **Language**: Python 3.11+
- **Data Storage**: JSON files (local persistence)
- **UI Components**: Streamlit built-in widgets

## Core Files Description

### 1. app.py (Main Application)
**Purpose**: Entry point and main navigation

**Key Features**:
- Multi-page application setup
- Sidebar navigation menu
- Quick statistics display
- Session state initialization
- Welcome page with health overview

**Main Functions**:
- `main()` - Application entry point
- `get_next_medicine_reminder()` - Calculate next medication
- `get_next_appointment()` - Get upcoming appointment
- `get_reminders_today_count()` - Count daily reminders

### 2. pages/1_Dashboard.py
**Purpose**: Health overview dashboard

**Features**:
- Health metrics summary cards
- Upcoming medicine reminders
- Recent medicines display
- Recent health data visualization
- Upcoming appointments list

**Main Functions**:
- `calculate_reminders_today()` - Daily reminder calculation
- `display_medicine_reminders()` - Show medication schedule
- `display_medicine_summary()` - Medicine overview
- `display_recent_health_data()` - Recent health metrics

### 3. pages/2_Medicines.py
**Purpose**: Complete medicine management system

**Features**:
- Add new medicines with full details
- Edit existing medications
- Delete medicines
- Filter by status (Active/Inactive/Completed)
- Search functionality
- Dosage and frequency tracking
- Next dose time scheduling

**Main Functions**:
- `display_medicines_list()` - Show all medicines with filters
- `add_medicine_form()` - Add new medicine
- `edit_medicine()` - Edit existing medicine
- `delete_medicine()` - Remove medicine

**Data Fields**:
- Name, dosage, frequency
- Prescriber information
- Status tracking
- Next dose time
- Start/end dates
- Notes and descriptions

### 4. pages/3_Appointments.py
**Purpose**: Doctor appointment scheduling and tracking

**Features**:
- Schedule new appointments
- Edit/delete appointments
- Filter by time period and doctor
- Color-coded status (upcoming/today/past)
- Reminder settings
- Insurance information

**Main Functions**:
- `display_appointments()` - Show appointments with filters
- `filter_appointments()` - Apply multiple filters
- `add_appointment_form()` - Schedule new appointment
- `edit_appointment()` - Modify existing appointment
- `delete_appointment()` - Remove appointment

**Data Fields**:
- Doctor name and specialty
- Date, time, location
- Reason for visit
- Contact and insurance
- Reminder preferences

### 5. pages/4_Health_Metrics.py
**Purpose**: Health vitals tracking and visualization

**Features**:
- Record multiple metric types
- Visual charts and trends
- Time range filtering
- Status indicators (normal/abnormal)
- Source tracking (manual/device/clinic)

**Supported Metrics**:
- Blood pressure (systolic/diastolic)
- Weight (kg/lbs)
- Heart rate (bpm)
- Blood sugar (mg/dL, mmol/L)
- Temperature (°C/°F)
- Oxygen saturation (%)
- Custom metrics

**Main Functions**:
- `display_metrics_overview()` - Metrics dashboard
- `display_metric_chart()` - Visualize trends
- `add_health_metric_form()` - Record new metric
- `display_metrics_history()` - Historical data view

### 6. pages/5_Family_Health.py
**Purpose**: Family member health profile management

**Features**:
- Add family member profiles
- Medical history tracking
- Allergies and conditions
- Insurance information
- Medicines and appointments per member

**Main Functions**:
- `display_family_members()` - Show all family profiles
- `view_member_profile()` - Detailed profile view
- `add_family_member_form()` - Add new member
- `edit_family_member()` - Update member info

**Data Fields**:
- Personal information (name, age, blood type)
- Medical conditions
- Allergies
- Insurance details
- Emergency contacts

### 7. pages/6_Emergency_SOS.py
**Purpose**: Emergency information and quick access

**Features**:
- Emergency contact management
- Critical medical information display
- Quick call buttons (demonstration)
- Medical profile settings
- Emergency activity logging

**Main Functions**:
- `emergency_quick_access()` - Quick action buttons
- `emergency_contacts_section()` - Contact management
- `medical_information_section()` - Critical info display
- `emergency_settings_section()` - Profile configuration
- `display_critical_medical_info()` - Emergency info card

### 8. utils/data_manager.py
**Purpose**: Data persistence layer

**Features**:
- JSON file read/write operations
- Data validation
- Backup and restore
- Import/export functionality
- Data statistics

**Main Methods**:
- `save_medicines()`, `load_medicines()`
- `save_appointments()`, `load_appointments()`
- `save_health_metrics()`, `load_health_metrics()`
- `save_family_members()`, `load_family_members()`
- `save_emergency_contacts()`, `load_emergency_contacts()`
- `save_medical_profile()`, `load_medical_profile()`
- `backup_data()` - Create backup
- `restore_data()` - Restore from backup
- `export_data()` - Export all data
- `import_data()` - Import data

### 9. utils/helpers.py
**Purpose**: Utility functions and helpers

**Key Functions**:

**Session Management**:
- `init_session_state()` - Initialize app state
- `sync_data()` - Sync to storage
- `clear_session_data()` - Reset data

**Data Retrieval**:
- `get_active_medicines()` - Active meds list
- `get_upcoming_appointments()` - Future appointments
- `get_recent_health_metrics()` - Recent metrics
- `get_medication_reminders()` - Today's reminders

**Formatting**:
- `format_date()` - Date formatting
- `format_time()` - Time formatting
- `format_medicine_frequency()` - Frequency display

**Calculations**:
- `calculate_age()` - Age from birthdate
- `calculate_bmi()` - BMI calculation
- `get_bmi_category()` - BMI classification
- `time_until()` - Time until target

**Validation**:
- `validate_phone_number()` - Phone validation
- `validate_email()` - Email validation

**Health Analysis**:
- `get_health_status_color()` - Status color coding
- `get_next_medicine_dose()` - Next dose calculation
- `get_emergency_info()` - Emergency data compilation

### 10. .streamlit/config.toml
**Purpose**: Streamlit configuration

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## Data Models

### Medicine Model
```python
{
    'name': str,
    'dosage': str,
    'frequency': str,
    'prescriber': str,
    'status': str,  # Active/Inactive/Completed
    'next_dose_time': str,  # HH:MM
    'start_date': str,  # YYYY-MM-DD
    'end_date': str,  # YYYY-MM-DD
    'description': str,
    'notes': str,
    'created_at': str,
    'updated_at': str
}
```

### Appointment Model
```python
{
    'doctor': str,
    'specialty': str,
    'date': str,  # YYYY-MM-DD
    'time': str,  # HH:MM
    'location': str,
    'reason': str,
    'contact': str,
    'insurance': str,
    'notes': str,
    'reminder': str,
    'created_at': str,
    'updated_at': str
}
```

### Health Metric Model
```python
{
    'type': str,  # blood_pressure, weight, etc.
    'value': str,
    'unit': str,
    'date': str,  # YYYY-MM-DD
    'time': str,  # HH:MM
    'source': str,  # manual, device, clinic
    'status': str,
    'location': str,
    'device': str,
    'notes': str,
    'created_at': str
}
```

### Family Member Model
```python
{
    'name': str,
    'relationship': str,
    'age': int,
    'gender': str,
    'date_of_birth': str,
    'blood_type': str,
    'phone': str,
    'emergency_contact': str,
    'medical_conditions': list,
    'allergies': list,
    'insurance': dict,
    'medicines': list,
    'appointments': list,
    'notes': str,
    'created_at': str,
    'updated_at': str
}
```

### Emergency Contact Model
```python
{
    'name': str,
    'phone': str,
    'email': str,
    'relationship': str,
    'address': str,
    'is_primary': bool,
    'is_medical': bool,
    'notes': str,
    'created_at': str
}
```

### Medical Profile Model
```python
{
    'blood_type': str,
    'age': int,
    'height': str,
    'weight': str,
    'emergency_contact_name': str,
    'emergency_contact_phone': str,
    'primary_doctor': str,
    'primary_doctor_phone': str,
    'conditions': list,
    'allergies': list,
    'special_instructions': str,
    'updated_at': str
}
```

## Data Flow

1. **User Interaction** → Streamlit UI
2. **Session State** → In-memory storage
3. **DataManager** → JSON file persistence
4. **Helpers** → Data processing & validation

## Key Design Patterns

### 1. Session State Management
- All data loaded at startup via `init_session_state()`
- Changes immediately reflected in session state
- Auto-saved to JSON files after modifications

### 2. Data Persistence
- Each data type has dedicated JSON file
- Automatic directory creation
- Error handling for file operations
- Backup/restore capabilities

### 3. Page Structure
- Each page is self-contained
- Imports only required utilities
- Consistent UI patterns
- Tab-based navigation within pages

### 4. Form Handling
- Streamlit forms for data entry
- Validation before submission
- Success/error feedback
- Auto-refresh on data changes

## Running the Application

### Local Development (VS Code)
```bash
# Install dependencies
pip install streamlit pandas

# Run application
streamlit run app.py --server.port 5000

# Or default port
streamlit run app.py
```

### Access
- Local: `http://localhost:5000`
- Network: `http://0.0.0.0:5000`

## File Dependencies

```
app.py
├── utils/data_manager.py
├── utils/helpers.py
└── .streamlit/config.toml

pages/1_Dashboard.py
├── utils/data_manager.py
└── utils/helpers.py

pages/2_Medicines.py
├── utils/data_manager.py
└── utils/helpers.py

pages/3_Appointments.py
├── utils/data_manager.py
└── utils/helpers.py

pages/4_Health_Metrics.py
├── utils/data_manager.py
└── utils/helpers.py

pages/5_Family_Health.py
├── utils/data_manager.py
└── utils/helpers.py

pages/6_Emergency_SOS.py
├── utils/data_manager.py
└── utils/helpers.py
```

## Data Storage

All data stored in `data/` directory:
- `medicines.json` - 💊 Medications
- `appointments.json` - 📅 Appointments
- `health_metrics.json` - 📈 Health data
- `family_members.json` - 👨‍👩‍👧‍👦 Family profiles
- `emergency_contacts.json` - 🚨 Emergency contacts
- `medical_profile.json` - 👤 Personal profile

## Security Considerations

- ✅ Local storage only (no cloud)
- ✅ No external API calls
- ✅ No user authentication (single user)
- ✅ Data stays on device
- ⚠️ No encryption (add for production)
- ⚠️ No multi-user support

## Customization Guide

### Adding New Metric Type
1. Edit `pages/4_Health_Metrics.py`
2. Add to metric type dropdown
3. Add value input handling
4. Update chart display logic

### Adding New Page
1. Create `pages/X_PageName.py`
2. Import utilities
3. Use `st.set_page_config()`
4. Add page navigation
5. Implement page logic

### Modifying Theme
Edit `.streamlit/config.toml`:
- `primaryColor` - Main accent
- `backgroundColor` - Main background
- `secondaryBackgroundColor` - Cards/containers
- `textColor` - Text color

## Performance Considerations

- JSON files load at startup
- Session state for fast access
- Minimal external dependencies
- Efficient data filtering
- Lightweight charts

## Error Handling

- Try-catch blocks for file operations
- Validation before data saves
- User-friendly error messages
- Fallback to defaults on load errors
- Graceful degradation

## Testing Recommendations

1. **Data Persistence**: Add/edit/delete items
2. **Filters**: Test all filter combinations
3. **Charts**: Verify metric visualizations
4. **Forms**: Validate required fields
5. **Navigation**: Test all page transitions

## Maintenance

- Backup `data/` folder regularly
- Monitor file sizes
- Clean old records periodically
- Update dependencies
- Test after Streamlit updates

---

**This is a complete, production-ready health management application suitable for personal use.**
