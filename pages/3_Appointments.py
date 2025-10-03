# pages/3_Appointments.py - FIXED VERSION
import streamlit as st
from datetime import datetime
import os
import sys

# Safe imports for utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_manager import DataManager
from utils.helpers import init_session_state
from api_client import APIClient  # FIXED: Correct import path
from utils.theme import apply_theme

st.set_page_config(page_title="Appointments - MedPal", page_icon="📅")
apply_theme()

def main():
    init_session_state()
    data_manager = DataManager()

    st.title("📅 Appointments")
    st.markdown("Schedule and manage your medical appointments")

    # Tabs for listing and scheduling
    tab1, tab2 = st.tabs(["📋 My Appointments", "➕ Schedule New"])

    with tab1:
        display_appointments(data_manager)

    with tab2:
        add_appointment_form(data_manager)


def display_appointments(data_manager: DataManager):
    """Display all appointments"""
    appointments = st.session_state.get("appointments", [])
    if not appointments:
        st.info("📋 No appointments scheduled yet. Use the 'Schedule New' tab.")
        return

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        time_filter = st.selectbox("Filter by Time", ["All", "Upcoming", "Past", "Today"])
    with col2:
        doctors = list(set([a.get("doctor", "") for a in appointments if a.get("doctor")]))
        doctor_filter = st.selectbox("Filter by Doctor", ["All"] + doctors)
    with col3:
        search_term = st.text_input("🔍 Search", placeholder="Search appointments...")

    # Apply filters
    filtered = filter_appointments(appointments, time_filter, doctor_filter, search_term)
    st.markdown(f"**Showing {len(filtered)} appointment(s)**")

    # Sort by date/time
    filtered.sort(key=lambda x: (x.get("date", ""), x.get("time", "")))
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Display each appointment
    for idx, apt in enumerate(filtered):
        # FIXED: Generate unique ID with fallback
        apt_id = apt.get("id", f"apt_{idx}")
        
        appointment_date = apt.get("date", "")
        appointment_time = apt.get("time", "")

        is_today = appointment_date == current_date
        is_past = appointment_date < current_date
        is_upcoming = appointment_date > current_date

        # Color coding
        border_color = "#51cf66"  # green default
        if is_today:
            border_color = "#ff6b6b"  # red
        elif is_past:
            border_color = "#d3d3d3"  # gray

        with st.container():
            st.markdown(
                f'<div style="border-left: 4px solid {border_color}; padding-left: 1rem; margin: 1rem 0;">',
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**🏥 {apt.get('doctor', 'Unknown Doctor')}**")
                st.write(f"📍 {apt.get('location', 'No location')}")
                if apt.get("specialty"):
                    st.write(f"🩺 {apt.get('specialty')}")
                if apt.get("reason"):
                    st.write(f"📝 {apt.get('reason')}")
                if apt.get("notes"):
                    st.caption(f"💭 {apt.get('notes')}")

            with col2:
                st.write(f"📅 **{appointment_date}**")
                st.write(f"🕐 **{appointment_time}**")
                if is_past:
                    st.info("Completed")
                elif is_today:
                    st.error("Today")
                else:
                    st.success("Upcoming")

            with col3:
                # FIXED: All buttons use unique, safe IDs
                if st.button("✏️ Edit", key=f"edit_apt_{apt_id}", use_container_width=True):
                    edit_appointment(idx, apt, data_manager)
                
                if st.button("🗑️ Delete", key=f"delete_apt_{apt_id}", use_container_width=True):
                    delete_appointment(idx, apt, data_manager)
                
                if is_upcoming or is_today:
                    if st.button("📞 Remind", key=f"remind_{apt_id}", use_container_width=True):
                        st.success("⏰ Reminder set! (Feature coming soon)")

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")


def filter_appointments(appointments, time_filter, doctor_filter, search_term):
    """Filter appointments by time, doctor, search term"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    filtered = appointments.copy()

    if time_filter == "Upcoming":
        filtered = [a for a in filtered if a.get("date", "") > current_date]
    elif time_filter == "Past":
        filtered = [a for a in filtered if a.get("date", "") < current_date]
    elif time_filter == "Today":
        filtered = [a for a in filtered if a.get("date", "") == current_date]

    if doctor_filter != "All":
        filtered = [a for a in filtered if a.get("doctor", "") == doctor_filter]

    if search_term:
        search_lower = search_term.lower()
        filtered = [
            a
            for a in filtered
            if search_lower in a.get("doctor", "").lower()
            or search_lower in a.get("location", "").lower()
            or search_lower in a.get("reason", "").lower()
            or search_lower in a.get("specialty", "").lower()
        ]

    return filtered


def add_appointment_form(data_manager: DataManager):
    """Form to add a new appointment"""
    st.subheader("Schedule New Appointment")

    with st.form("add_appointment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            doctor = st.text_input("Doctor Name *", placeholder="e.g., Dr. Smith")
            specialty = st.text_input("Specialty", placeholder="e.g., Cardiologist")
            date = st.date_input(
                "Appointment Date *",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )
            time = st.time_input(
                "Appointment Time *",
                value=datetime.strptime("09:00", "%H:%M").time()
            )
        
        with col2:
            location = st.text_input("Location", placeholder="e.g., City Hospital, Room 301")
            reason = st.text_input("Reason", placeholder="e.g., Annual checkup")
            contact = st.text_input("Contact", placeholder="e.g., +1 234 567 8900")
            insurance = st.text_input("Insurance", placeholder="e.g., Blue Cross")
        
        notes = st.text_area("Additional Notes", placeholder="Any special instructions...")

        submitted = st.form_submit_button("📅 Schedule Appointment", use_container_width=True)
        
        if submitted:
            if not doctor or not date or not time:
                st.error("❌ Please fill in all required fields (marked with *)")
                return
            
            new_appointment = {
                "doctor": doctor,
                "specialty": specialty,
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%H:%M"),
                "location": location,
                "reason": reason,
                "contact": contact,
                "insurance": insurance,
                "notes": notes,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Try to save to backend first
            client = APIClient()
            client.token = st.session_state.get("auth_token")  # FIXED: Correct key name
            
            try:
                resp = client.add_appointment(new_appointment)
                
                if resp and "id" in resp:
                    new_appointment["id"] = resp["id"]
                    st.session_state.setdefault("appointments", []).append(new_appointment)
                    data_manager.save_appointments(st.session_state.appointments)
                    st.success(f"✅ Appointment with {doctor} scheduled successfully!")
                    st.rerun()
                else:
                    # Save locally even if backend fails
                    st.warning("⚠️ Saved locally (backend unavailable)")
                    new_appointment["id"] = f"local_{datetime.now().timestamp()}"
                    st.session_state.setdefault("appointments", []).append(new_appointment)
                    data_manager.save_appointments(st.session_state.appointments)
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error saving appointment: {e}")


def edit_appointment(index: int, appointment: dict, data_manager: DataManager):
    """Edit appointment details"""
    st.markdown("---")
    st.subheader("✏️ Edit Appointment")
    
    with st.form(f"edit_appointment_form_{index}"):
        col1, col2 = st.columns(2)
        
        with col1:
            doctor = st.text_input("Doctor Name", value=appointment.get("doctor", ""))
            specialty = st.text_input("Specialty", value=appointment.get("specialty", ""))
            
            # Parse existing date
            try:
                existing_date = datetime.strptime(appointment.get("date", ""), "%Y-%m-%d").date()
            except:
                existing_date = datetime.now().date()
            date = st.date_input("Date", value=existing_date)
            
            # Parse existing time
            try:
                existing_time = datetime.strptime(appointment.get("time", "09:00"), "%H:%M").time()
            except:
                existing_time = datetime.strptime("09:00", "%H:%M").time()
            time = st.time_input("Time", value=existing_time)
        
        with col2:
            location = st.text_input("Location", value=appointment.get("location", ""))
            reason = st.text_input("Reason", value=appointment.get("reason", ""))
            contact = st.text_input("Contact", value=appointment.get("contact", ""))
            insurance = st.text_input("Insurance", value=appointment.get("insurance", ""))
        
        notes = st.text_area("Notes", value=appointment.get("notes", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            update = st.form_submit_button("💾 Save Changes", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if update:
            updated = appointment.copy()
            updated.update({
                "doctor": doctor,
                "specialty": specialty,
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%H:%M"),
                "location": location,
                "reason": reason,
                "contact": contact,
                "insurance": insurance,
                "notes": notes,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.session_state.appointments[index] = updated
            data_manager.save_appointments(st.session_state.appointments)
            st.success("✅ Appointment updated!")
            st.rerun()
        
        if cancel:
            st.rerun()


def delete_appointment(index: int, appointment: dict, data_manager: DataManager):
    """Delete appointment from both backend and local storage"""
    client = APIClient()
    client.token = st.session_state.get("auth_token")  # FIXED: Correct key name

    try:
        # Try to delete from backend if it has an ID
        if appointment.get("id") and not str(appointment["id"]).startswith("local_"):
            resp = client.delete_appointment(appointment["id"])
            if resp and "message" in resp:
                st.success("✅ Deleted from server")
        
        # Delete from local state
        del st.session_state.appointments[index]
        data_manager.save_appointments(st.session_state.appointments)
        st.success(f"✅ Appointment with {appointment.get('doctor', 'Unknown')} deleted")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error deleting appointment: {e}")


if __name__ == "__main__":
    main()