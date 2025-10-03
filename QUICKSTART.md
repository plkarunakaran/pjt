# MedPal - Quick Start Guide

## Running the Application Locally in VS Code

### Step 1: Open the Project
1. Open VS Code
2. Open the project folder containing all the MedPal files

### Step 2: Install Required Packages
Open the terminal in VS Code (Terminal → New Terminal) and run:

```bash
pip install streamlit pandas
```

### Step 3: Run the Application
In the terminal, execute:

```bash
streamlit run app.py --server.port 5000
```

Or simply:

```bash
streamlit run app.py
```

### Step 4: Access the Application
- The application will automatically open in your browser
- If not, navigate to: `http://localhost:8501` (or the port shown in the terminal)

## File Structure for VS Code

When you open the project in VS Code, you'll see:

```
📁 Your Project Folder
├── 📄 app.py                    # Main application
├── 📁 pages/                    # All pages
│   ├── 1_Dashboard.py
│   ├── 2_Medicines.py
│   ├── 3_Appointments.py
│   ├── 4_Health_Metrics.py
│   ├── 5_Family_Health.py
│   └── 6_Emergency_SOS.py
├── 📁 utils/                    # Utilities
│   ├── data_manager.py
│   └── helpers.py
├── 📁 .streamlit/              # Config
│   └── config.toml
├── 📁 data/                    # Auto-created data folder
└── 📄 README.md                # Documentation
```

## Quick Commands

### Install Dependencies
```bash
pip install streamlit pandas
```

### Run Application
```bash
streamlit run app.py
```

### Stop Application
- Press `Ctrl+C` in the terminal

### Clear Cache (if needed)
```bash
streamlit cache clear
```

## First Time Setup

1. **Run the application** - First time will create the `data/` folder automatically
2. **Navigate through pages** - Use the sidebar to explore different sections
3. **Add your first medicine** - Go to "My Medicines" → "Add New Medicine"
4. **Set up emergency profile** - Go to "Emergency SOS" → "Settings"

## VS Code Extensions (Optional but Recommended)

For better development experience, install:
- Python (Microsoft)
- Pylance (Microsoft)

## Data Storage Location

All your health data is stored in the `data/` folder as JSON files:
- `medicines.json` - Your medications
- `appointments.json` - Your appointments
- `health_metrics.json` - Your health measurements
- `family_members.json` - Family profiles
- `emergency_contacts.json` - Emergency contacts
- `medical_profile.json` - Your medical profile

## Backup Your Data

To backup your data, simply copy the entire `data/` folder to a safe location.

## Troubleshooting

**Issue: Module not found error**
```bash
pip install streamlit pandas
```

**Issue: Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Issue: Application won't start**
1. Make sure Python 3.11+ is installed
2. Verify all files are in the correct structure
3. Check terminal for error messages

## Need Help?

Refer to the comprehensive `README.md` file for detailed documentation.

---

**That's it! You're ready to start managing your health with MedPal!** 🏥
