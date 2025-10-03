# app.py - Enhanced version with Dark Mode
import streamlit as st
from datetime import datetime
from api_client import APIClient


st.set_page_config(
    page_title="MedPal - Your Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ADDED: Dark Mode Configuration

def apply_theme():
    """Apply dark or light theme based on session state"""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    if st.session_state.dark_mode:
        # Dark mode CSS - Lighter background, bright white text
        st.markdown("""
        <style>
            /* Main background - lighter dark gray */
            .stApp {
                background-color: #1e1e1e !important;
                color: #ffffff !important;
            }
            
            /* All text elements - bright white */
            .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
                color: #ffffff !important;
            }
            
            /* Title and headers */
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }
            
            /* All paragraph text */
            p, span, div {
                color: #ffffff !important;
            }
            
            /* Info/Warning/Success boxes text */
            .stAlert p, .stAlert span, .stAlert div {
                color: #ffffff !important;
            }
            
            /* Buttons */
            .stButton>button {
                width: 100%;
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
                border-radius: 12px !important;
            }
            .stButton>button:hover {
                background-color: #404040 !important;
                border-color: #505050 !important;
            }
            
            /* Input fields */
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
                border-radius: 12px !important;
            }
            
            /* Selectbox */
            .stSelectbox>div>div>div {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border-radius: 12px !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #2d2d2d !important;
            }
            [data-testid="stSidebar"] * {
                color: #ffffff !important;
            }
            
            /* Metrics */
            .stMetric {
                background-color: #2d2d2d !important;
                padding: 1rem !important;
                border-radius: 16px !important;
                border: 1px solid #404040 !important;
            }
            div[data-testid="stMetricValue"] {
                color: #ffffff !important;
            }
            div[data-testid="stMetricLabel"] {
                color: #ffffff !important;
            }
            
            /* Alerts */
            .stAlert, .stWarning, .stSuccess, .stInfo, .stError {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
                border-radius: 16px !important;
                padding: 1rem !important;
            }
            
            /* Expander */
            .stExpander {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
                border-radius: 12px !important;
            }
            
            /* Cards */
            .metric-card {
                background: #2d2d2d !important;
                padding: 1rem;
                border-radius: 16px;
                margin: 0.5rem 0;
                color: #ffffff !important;
                border: 1px solid #404040;
            }
            
            /* Forms */
            .stForm {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
                border-radius: 16px !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2d2d2d !important;
                border-radius: 12px !important;
            }
            .stTabs [data-baseweb="tab"] {
                color: #ffffff !important;
                border-radius: 8px !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light mode CSS
        st.markdown("""
        <style>
            .stButton>button {
                width: 100%;
            }
            .metric-card {
                background: #f0f2f6;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
            }
        </style>
        """, unsafe_allow_html=True)

# Apply theme
apply_theme()


def main():
    """Main application entry point"""
    # Initialize API client
    if "api_client" not in st.session_state:
        st.session_state.api_client = APIClient()
    
    client = st.session_state.api_client

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "auth_token" in st.session_state and st.session_state.auth_token:
        client.token = st.session_state.auth_token
        st.session_state.logged_in = True

    if not st.session_state.logged_in:
        show_auth_page(client)
    else:
        show_dashboard(client)


def show_auth_page(client: APIClient):
    """Display login/signup page"""
    st.title("🔐 Welcome to MedPal")
    st.markdown("### Your Personal Health Management System")
    
    # ADDED: Dark mode toggle on auth page
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.info("📱 Track medicines, appointments, and health metrics in one place")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        show_login_form(client)
    
    with tab2:
        show_signup_form(client)


def show_login_form(client: APIClient):
    """Display login form"""
    st.subheader("Login to Your Account")
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
        with col2:
            st.form_submit_button("Clear", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("Please enter both username and password")
                return
            
            with st.spinner("Logging in..."):
                success = client.login(username, password)
            
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Login failed. Please check your credentials and try again.")


def show_signup_form(client: APIClient):
    """Display signup form"""
    st.subheader("Create New Account")
    
    with st.form("signup_form", clear_on_submit=True):
        full_name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Email *", placeholder="your.email@example.com")
        username = st.text_input("Username *", placeholder="Choose a username")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password *", type="password", placeholder="Min. 6 characters")
        with col2:
            password_confirm = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password")
        
        st.caption("* Required fields")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        
        if submitted:
            if not all([full_name, email, username, password]):
                st.error("Please fill in all required fields")
                return
            
            if password != password_confirm:
                st.error("Passwords do not match")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return
            
            if "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address")
                return
            
            with st.spinner("Creating account..."):
                user = client.signup(username, email, password, full_name)
            
            if user and "id" in user:
                st.success("Account created successfully! Please login with your credentials.")
                st.balloons()
            else:
                error_msg = user.get("error", "Unknown error") if isinstance(user, dict) else "Failed to create account"
                st.error(f"Signup failed: {error_msg}")


def show_dashboard(client: APIClient):
    """Display main dashboard"""
    medicines = fetch_medicines(client)
    appointments = fetch_appointments(client)
    health_metrics = fetch_health_metrics(client)

    # Sidebar
    with st.sidebar:
        st.title("🏥 MedPal")
        st.markdown("*Your Health Companion*")
        st.markdown("---")
        
        # ADDED: Dark Mode Toggle
        theme_icon = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
        if st.button(theme_icon, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        username = st.session_state.get('username', 'User')
        st.markdown(f"**👤 {username}**")
        st.caption(f"Last login: {datetime.now().strftime('%B %d, %Y')}")
        
        st.markdown("---")
        
        st.markdown("### 📊 Quick Stats")
        
        active_meds = len([m for m in medicines if m.get('status', '').lower() == 'active'])
        upcoming_apts = len([a for a in appointments if a.get('date', '') >= datetime.now().strftime('%Y-%m-%d')])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Medicines", active_meds)
            st.metric("Health Records", len(health_metrics))
        with col2:
            st.metric("Appointments", upcoming_apts)
            st.metric("Contacts", 0)
        
        st.markdown("---")
        
        st.info("Use the sidebar pages to navigate to different sections")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Main Content
    st.title(f"Welcome back, {st.session_state.get('username', 'User')}!")
    st.markdown("### Your Health Dashboard")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💊 Medicines")
        if active_meds > 0:
            st.success(f"{active_meds} active medication(s)")
            next_med = get_next_medicine_reminder(medicines)
            if next_med:
                st.info(f"Next: {next_med['name']} at {next_med.get('next_dose_time', 'N/A')}")
        else:
            st.warning("No active medicines")
        
        if st.button("Manage Medicines", key="btn_medicines"):
            st.switch_page("pages/2_Medicines.py")
    
    with col2:
        st.markdown("#### 📅 Appointments")
        if upcoming_apts > 0:
            st.success(f"{upcoming_apts} upcoming")
            next_appt = get_next_appointment(appointments)
            if next_appt:
                st.info(f"Next: {next_appt['doctor']}\n{next_appt['date']}")
        else:
            st.warning("No upcoming appointments")
        
        if st.button("View Appointments", key="btn_appointments"):
            st.switch_page("pages/3_Appointments.py")
    
    with col3:
        st.markdown("#### 📊 Health")
        if len(health_metrics) > 0:
            st.success(f"{len(health_metrics)} record(s)")
            st.info("Track your vitals")
        else:
            st.warning("No health records")
        
        if st.button("Health Metrics", key="btn_health"):
            st.info("Health metrics page coming soon!")

    st.markdown("---")
    st.markdown("### 🚨 Emergency SOS")
    
    with st.expander("Send Emergency Alert", expanded=False):
        st.warning("⚠️ For real emergencies, call 911 or your local emergency number immediately")
        
        sos_message = st.text_area(
            "Emergency Message",
            value="Emergency! I need immediate help.",
            placeholder="Describe your emergency...",
            height=100
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🚨 Send Emergency SOS", type="primary", use_container_width=True):
                with st.spinner("Sending emergency alert..."):
                    resp = client.send_sos(sos_message)
                
                if resp and not resp.get("error"):
                    st.success("Emergency alert sent successfully!")
                    
                    if resp.get("simulation"):
                        st.info("📱 Demo Mode: Twilio credentials not configured. Add them to .env file for real SMS.")
                    
                    st.write(f"**Contacts Notified:** {resp.get('contacts_notified', 0)}")
                    
                    if resp.get("sent_to"):
                        st.write("**Alert sent to:**")
                        for contact in resp["sent_to"]:
                            st.write(f"✓ {contact}")
                else:
                    st.error("Failed to send emergency alert")
                    if resp and resp.get("error"):
                        st.error(f"Error: {resp['error']}")
        
        with col2:
            if st.button("📞 Emergency Contacts", use_container_width=True):
                st.switch_page("pages/4_Emergency_SOS.py")

    st.markdown("---")
    st.markdown("### 📋 Recent Activity")
    
    if medicines or appointments:
        recent_items = []
        
        for med in medicines[:3]:
            recent_items.append({
                "type": "Medicine",
                "icon": "💊",
                "title": med.get('name', 'Unknown'),
                "subtitle": f"{med.get('dosage', 'N/A')} - {med.get('status', 'Unknown')}"
            })
        
        for apt in appointments[:3]:
            recent_items.append({
                "type": "Appointment",
                "icon": "📅",
                "title": apt.get('doctor', 'Unknown'),
                "subtitle": f"{apt.get('date', 'N/A')} at {apt.get('time', 'N/A')}"
            })
        
        for item in recent_items[:5]:
            st.markdown(f"{item['icon']} **{item['title']}** - {item['subtitle']}")
    else:
        st.info("No recent activity. Start by adding medicines or appointments!")


def fetch_medicines(client: APIClient) -> list:
    try:
        medicines = client.get_medicines()
        return medicines if isinstance(medicines, list) else []
    except Exception as e:
        st.error(f"Failed to load medicines: {str(e)}")
        return []


def fetch_appointments(client: APIClient) -> list:
    try:
        appointments = client.get_appointments()
        return appointments if isinstance(appointments, list) else []
    except Exception as e:
        st.error(f"Failed to load appointments: {str(e)}")
        return []


def fetch_health_metrics(client: APIClient) -> list:
    try:
        metrics = client.get_health_metrics()
        return metrics if isinstance(metrics, list) else []
    except Exception as e:
        st.error(f"Failed to load health metrics: {str(e)}")
        return []


def get_next_medicine_reminder(medicines: list) -> dict:
    active = [m for m in medicines if m.get('status', '').lower() == 'active']
    
    if not active:
        return None
    
    active.sort(key=lambda x: x.get('next_dose_time', '23:59'))
    return active[0] if active else None


def get_next_appointment(appointments: list) -> dict:
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [a for a in appointments if a.get('date', '') >= today]
    
    if not upcoming:
        return None
    
    upcoming.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))
    return upcoming[0] if upcoming else None


if __name__ == "__main__":
    main()