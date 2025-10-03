import streamlit as st
from datetime import datetime
from api_client import APIClient
from utils.helpers import format_time_until
from utils.theme import apply_theme

st.set_page_config(page_title="Dashboard - MedPal", page_icon="📊")
apply_theme()
def main():
    # Get client from session
    client: APIClient = st.session_state.get("api_client")
    if not client:
        st.error("⚠️ Please login first from the main app.")
        st.stop()

    st.title("📊 Health Dashboard")
    st.markdown("Welcome back! Here's your health overview for today")

    # Fetch data from API
    medicines = client.get_medicines() or []
    appointments = client.get_appointments() or []
    health_metrics = client.get_health_metrics() or []

    # Quick actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Medicine", use_container_width=True):
            st.switch_page("pages/2_Medicines.py")
    with col2:
        if st.button("📅 New Appointment", use_container_width=True):
            st.switch_page("pages/3_Appointments.py")

    st.markdown("---")

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    active_medicines = len([m for m in medicines if m.get("status") == "Active"])
    today = datetime.now().strftime("%Y-%m-%d")
    upcoming_appointments = len([a for a in appointments if a.get("date", "") >= today])
    health_records = len(health_metrics)
    reminders_today = calculate_reminders_today(medicines)

    with col1:
        st.metric("Active Medicines", active_medicines)
    with col2:
        st.metric("Upcoming Appointments", upcoming_appointments)
    with col3:
        st.metric("Health Records", health_records)
    with col4:
        st.metric("Reminders Today", reminders_today)

    # Sections
    st.markdown("---")
    st.subheader("💊 My Medicines")
    if medicines:
        display_medicine_summary(medicines)
    else:
        st.info("No medicines added yet.")

    st.markdown("---")
    st.subheader("📈 Recent Health Data")
    if health_metrics:
        display_recent_health_data(health_metrics)
    else:
        st.info("No health metrics recorded yet.")

    st.markdown("---")
    st.subheader("📅 Upcoming Appointments")
    display_appointments(appointments)

def calculate_reminders_today(medicines):
    """Count reminders for today"""
    active_medicines = [m for m in medicines if m.get("status") == "Active"]
    total = 0
    for med in active_medicines:
        freq = med.get("frequency", "").lower()
        if "once" in freq: total += 1
        elif "twice" in freq: total += 2
        elif "three" in freq or "thrice" in freq: total += 3
        else: total += 1
    return total

def display_medicine_summary(medicines):
    for med in medicines[:3]:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{med.get('name', 'Unknown')}**")
                st.write(f"{med.get('dosage', 'Unknown dosage')} - {med.get('frequency', 'Unknown frequency')}")
                if med.get("prescriber"):
                    st.write(f"Prescribed by {med['prescriber']}")
                if med.get("next_dose_time"):
                    st.write(f"Next dose at {med['next_dose_time']}")
            with col2:
                status = med.get("status", "Unknown")
                if status == "Active":
                    st.success(status)
                else:
                    st.info(status)
        st.markdown("---")

def display_recent_health_data(metrics):
    sorted_metrics = sorted(metrics, key=lambda x: x.get("date", ""), reverse=True)
    for m in sorted_metrics[:4]:
        col1, col2, col3, col4 = st.columns([2,2,2,2])
        with col1: st.write(f"**{m.get('type', 'Unknown').title()}**")
        with col2: st.write(f"{m.get('value','')} {m.get('unit','')}")
        with col3: st.write(f"{m.get('date','')} {m.get('time','')}")
        with col4: st.caption(m.get("source","manual"))
        if m.get("notes"): st.caption(m["notes"])
        st.markdown("---")

def display_appointments(appointments):
    today = datetime.now().strftime("%Y-%m-%d")
    upcoming = [a for a in appointments if a.get("date", "") >= today]
    if not upcoming:
        st.info("No upcoming appointments.")
        return
    for a in upcoming[:3]:
        col1, col2, col3 = st.columns([2,2,1])
        with col1: st.write(f"**{a.get('doctor','Unknown Doctor')}**")
        with col2: st.write(a.get("date","No date"))
        with col3: st.write(a.get("time","No time"))

if __name__ == "__main__":
    main()
