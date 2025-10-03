# utils/theme.py - Theme configuration for all pages
import streamlit as st


def apply_theme():
    """Apply dark or light theme based on session state - Works on ALL pages"""
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
                border-radius: 0.5rem !important;
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
            }
            
            /* Expander */
            .stExpander {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
            }
            
            /* Cards */
            .metric-card {
                background: #2d2d2d !important;
                padding: 1rem;
                border-radius: 0.5rem;
                margin: 0.5rem 0;
                color: #ffffff !important;
                border: 1px solid #404040;
            }
            
            /* Forms */
            .stForm {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2d2d2d !important;
            }
            .stTabs [data-baseweb="tab"] {
                color: #ffffff !important;
            }
            
            /* Dataframe */
            .stDataFrame {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
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


def dark_mode_toggle():
    """Add dark mode toggle button"""
    theme_icon = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(theme_icon, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()