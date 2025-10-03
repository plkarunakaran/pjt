# MedPal - Your Health Companion

A comprehensive health management application built with Python and Streamlit. Track medications, appointments, health metrics, family health profiles, and emergency information all in one place.

## Features

### 1. Dashboard
- Health overview with key metrics
- Active medicines count
- Upcoming appointments
- Health records tracking
- Quick action buttons

### 2. Medicine Management
- Add, edit, and delete medications
- Track dosage, frequency, and prescriber information
- Set next dose times and reminders
- Filter by status (Active/Inactive/Completed)
- Search functionality

### 3. Appointments
- Schedule and manage doctor appointments
- Track appointment details (doctor, specialty, location, reason)
- Set reminders (1 hour to 1 week before)
- Filter by time period and doctor
- Color-coded status indicators (upcoming, today, past)

### 4. Health Metrics Tracking
- Record blood pressure, weight, heart rate, blood sugar
- Support for additional metrics (temperature, oxygen saturation)
- Visual charts and trend analysis
- Filter by time range and source
- Status indicators for abnormal values

### 5. Family Health Profiles
- Manage health profiles for family members
- Track medical conditions and allergies
- Store insurance information
- Record medications and appointments for each member
- Emergency contact information

### 6. Emergency SOS
- Quick access to emergency contacts
- Critical medical information display
- Emergency action buttons
- Medical profile management
- Activity logging

## Project Structure

```
medpal/
├── app.py                          # Main application entry point
├── pages/                          # Streamlit pages
│   ├── 1_Dashboard.py             # Dashboard page
│   ├── 2_Medicines.py             # Medicine management
│   ├── 3_Appointments.py          # Appointments management
│   ├── 4_Health_Metrics.py        # Health metrics tracking
│   ├── 5_Family_Health.py         # Family health profiles
│   └── 6_Emergency_SOS.py         # Emergency information
├── utils/                          # Utility modules
│   ├── data_manager.py            # Data persistence layer
│   └── helpers.py                 # Helper functions
├── .streamlit/                     # Streamlit configuration
│   └── config.toml                # Server configuration
├── data/                           # Data storage (auto-created)
│   ├── medicines.json
│   ├── appointments.json
│   ├── health_metrics.json
│   ├── family_members.json
│   ├── emergency_contacts.json
│   └── medical_profile.json
└── README.md                       # This file
```

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
If you have the project files, navigate to the project directory:
```bash
cd medpal
```

### Step 2: Install Dependencies
```bash
pip install streamlit pandas
```

### Step 3: Run the Application
```bash
streamlit run app.py --server.port 5000
```

The application will open in your default browser at `http://localhost:5000`

## Configuration

The application uses Streamlit's configuration system. The `.streamlit/config.toml` file contains:

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

## Data Storage

MedPal uses local JSON files for data persistence. All data is stored in the `data/` directory:

- **medicines.json**: Medication records
- **appointments.json**: Appointment schedules
- **health_metrics.json**: Health measurements
- **family_members.json**: Family health profiles
- **emergency_contacts.json**: Emergency contact information
- **medical_profile.json**: Personal medical profile

## Usage Guide

### Adding a Medicine
1. Go to "My Medicines" page
2. Click "Add New Medicine" tab
3. Fill in required fields (name, dosage, frequency)
4. Optionally add prescriber, notes, and end date
5. Click "Add Medicine"

### Scheduling an Appointment
1. Go to "Appointments" page
2. Click "Schedule New" tab
3. Enter doctor name, date, and time
4. Add location, reason, and insurance details
5. Set reminder preferences
6. Click "Schedule Appointment"

### Recording Health Metrics
1. Go to "Health Metrics" page
2. Click "Record New" tab
3. Select metric type (blood pressure, weight, etc.)
4. Enter value and date/time
5. Add source and notes
6. Click "Record Metric"

### Setting Up Emergency Profile
1. Go to "Emergency SOS" page
2. Navigate to "Settings" tab
3. Fill in personal medical information
4. Add medical conditions and allergies
5. Set emergency contact information
6. Click "Save Medical Profile"

## Key Features Explained

### Data Persistence
- Automatic saving to JSON files
- Session state management
- Data backup and restore functionality
- Export/import capabilities

### Health Metrics Analysis
- Visual charts for trend analysis
- Time range filtering (7, 30, 90 days, all time)
- Status indicators for abnormal values
- Support for multiple measurement sources

### Medicine Reminders
- Next dose time calculation
- Frequency-based scheduling
- Daily reminder counts
- Status tracking (Active/Inactive/Completed)

### Family Health Management
- Individual profiles for family members
- Medical history tracking
- Insurance information storage
- Relationship mapping

## Development

### File Overview

#### app.py
Main application entry point with:
- Page configuration
- Navigation sidebar
- Quick stats display
- Welcome page layout

#### utils/data_manager.py
Handles all data persistence:
- JSON file read/write operations
- Data validation
- Backup/restore functionality
- Import/export features

#### utils/helpers.py
Utility functions for:
- Session state initialization
- Date/time formatting
- Health status calculations
- Data filtering and searching
- BMI calculations

### Adding New Features

To add a new page:
1. Create a new file in `pages/` directory (e.g., `7_New_Feature.py`)
2. Use `st.set_page_config()` at the top
3. Import required utilities
4. Implement page logic
5. Add to navigation in `app.py` if needed

## Data Security

**Important Notes:**
- All data is stored locally in JSON files
- No cloud synchronization
- No external data transmission
- Suitable for personal use
- For production use, consider database encryption

## Troubleshooting

### Application won't start
- Ensure Python 3.11+ is installed: `python --version`
- Install dependencies: `pip install streamlit pandas`
- Check port 5000 is available

### Data not saving
- Verify `data/` directory exists and has write permissions
- Check for error messages in the terminal
- Ensure JSON files are not corrupted

### Pages not loading
- Clear browser cache
- Restart the application
- Check for error messages in Streamlit logs

## Future Enhancements

Potential features for future versions:
- Medication reminder notifications
- Health metrics visualization with advanced charts
- Prescription photo upload
- PDF health reports export
- Calendar app integration
- Cloud backup options
- Multi-user support
- Mobile app version

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the usage guide
3. Examine the code comments for detailed functionality

## License

This project is provided as-is for personal health management use.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data analysis
- Python 3.11+ - Core language

---

**Disclaimer**: This application is for personal health tracking only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.
