# pages/2_Medicines.py - FIXED
import streamlit as st
from datetime import datetime
import sys
import os

# Safe import of utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_manager import DataManager
from utils.helpers import init_session_state, get_urgent_reminders, format_time_until
from api_client import APIClient
from utils.theme import apply_theme


st.set_page_config(page_title="My Medicines - MedPal", page_icon="💊")
apply_theme()




def main():
    # Check authentication
    if not st.session_state.get("logged_in"):
        st.error("Please login first")
        st.stop()
    
    init_session_state()
    data_manager = DataManager()
    
    st.title("💊 My Medicines")
    st.markdown("Manage your medications and track dosages")
    
    # Display urgent reminders
    display_reminder_notifications()
    
    # Tabs
    tab1, tab2 = st.tabs(["📋 Medicine List", "➕ Add New Medicine"])
    
    with tab1:
        display_medicines_list(data_manager)
    
    with tab2:
        add_medicine_form(data_manager)


def display_reminder_notifications():
    """Show urgent reminders at top"""
    try:
        urgent_reminders = get_urgent_reminders()
        if not urgent_reminders:
            return
        
        for reminder in urgent_reminders[:3]:
            medicine = reminder["medicine"]
            urgency = reminder["urgency"]
            time_until = format_time_until(reminder["time_until"])
            
            if urgency == "overdue":
                st.error(f"⚠️ **OVERDUE**: {medicine.get('name')} ({medicine.get('dosage')}) - Was due at {medicine.get('next_dose_time')}")
            elif urgency == "urgent":
                st.warning(f"🔔 **URGENT**: {medicine.get('name')} ({medicine.get('dosage')}) - Due in {time_until}")
            elif urgency == "soon":
                st.info(f"📌 **UPCOMING**: {medicine.get('name')} ({medicine.get('dosage')}) - Due in {time_until}")
    except Exception as e:
        st.error(f"Error loading reminders: {e}")


def display_medicines_list(data_manager: DataManager):
    """Display list of medicines with filters"""
    medicines = st.session_state.get("medicines", [])
    
    if not medicines:
        st.info("📋 No medicines added yet. Use the 'Add New Medicine' tab to get started.")
        return

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "Completed"])
    with col2:
        search_term = st.text_input("🔍 Search", placeholder="Enter medicine name...")

    # Apply filters
    filtered = medicines.copy()
    if status_filter != "All":
        filtered = [m for m in filtered if m.get("status") == status_filter]
    if search_term:
        filtered = [m for m in filtered if search_term.lower() in m.get("name", "").lower()]

    st.markdown(f"**Showing {len(filtered)} medicine(s)**")

    # Display each medicine
    for idx, med in enumerate(filtered):
        # Create unique ID for this medicine - MOVED OUTSIDE EXPANDER
        med_id = med.get('id', f"med_{idx}")
        
        with st.expander(f"💊 {med.get('name', 'Unknown')} - {med.get('dosage', 'N/A')}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Dosage:** {med.get('dosage', 'Not specified')}")
                st.write(f"**Frequency:** {med.get('frequency', 'Not specified')}")
                
                if med.get("prescriber"):
                    st.write(f"**Prescriber:** {med.get('prescriber')}")
                if med.get("next_dose_time"):
                    st.write(f"**Next dose:** {med.get('next_dose_time')}")
                if med.get("start_date"):
                    st.write(f"**Start date:** {med.get('start_date')}")
                if med.get("end_date"):
                    st.write(f"**End date:** {med.get('end_date')}")
                if med.get("notes"):
                    st.caption(f"📝 {med.get('notes')}")

            with col2:
                # Status badge
                status = med.get("status", "Unknown")
                if status == "Active":
                    st.success(f"✅ {status}")
                elif status == "Inactive":
                    st.warning(f"⏸️ {status}")
                else:
                    st.info(f"📋 {status}")

                # Action buttons with UNIQUE keys - FIXED (removed duplicate med_id line)
                if st.button("✏️ Edit", key=f"edit_{med_id}", use_container_width=True):
                    show_edit_form(idx, med, data_manager)
                
                if st.button("🗑️ Delete", key=f"delete_{med_id}", use_container_width=True):
                    delete_medicine(idx, med, data_manager)


def show_edit_form(index: int, medicine: dict, data_manager: DataManager):
    """Display edit form for medicine"""
    st.markdown("---")
    st.subheader("Edit Medicine")
    
    with st.form(f"edit_medicine_form_{index}"):
        name = st.text_input("Medicine Name", value=medicine.get("name", ""))
        dosage = st.text_input("Dosage", value=medicine.get("dosage", ""))
        
        frequencies = ["Once daily", "Twice daily", "Three times daily", "As needed"]
        current_freq = medicine.get("frequency", "Once daily")
        try:
            freq_index = frequencies.index(current_freq)
        except ValueError:
            freq_index = 0
            
        frequency = st.selectbox("Frequency", frequencies, index=freq_index)
        
        statuses = ["Active", "Inactive", "Completed"]
        current_status = medicine.get("status", "Active")
        try:
            status_index = statuses.index(current_status)
        except ValueError:
            status_index = 0
            
        status = st.selectbox("Status", statuses, index=status_index)
        
        if st.form_submit_button("Save Changes"):
            # Update medicine
            updated = medicine.copy()
            updated.update({
                "name": name,
                "dosage": dosage,
                "frequency": frequency,
                "status": status,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            st.session_state.medicines[index] = updated
            data_manager.save_medicines(st.session_state.medicines)
            st.success("Medicine updated successfully!")
            st.rerun()


def delete_medicine(index: int, medicine: dict, data_manager: DataManager):
    """Delete medicine from both backend and local storage"""
    client = APIClient()
    client.token = st.session_state.get("auth_token")

    try:
        # If medicine has ID, try to delete from backend
        if medicine.get("id") and isinstance(medicine.get("id"), int):
            resp = client.delete_medicine(medicine["id"])
            if resp and "message" in resp:
                st.success(f"✅ Deleted {medicine.get('name')} from server")
        
        # Remove from local state
        if index < len(st.session_state.medicines):
            del st.session_state.medicines[index]
            data_manager.save_medicines(st.session_state.medicines)
            st.success(f"✅ {medicine.get('name', 'Medicine')} deleted")
            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error deleting medicine: {e}")


def add_medicine_form(data_manager: DataManager):
    """Form to add new medicine"""
    st.subheader("Add New Medicine")
    
    with st.form("add_medicine_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Medicine Name *", placeholder="e.g., Aspirin")
            dosage = st.text_input("Dosage *", placeholder="e.g., 500mg")
            frequency = st.selectbox(
                "Frequency *",
                ["Once daily", "Twice daily", "Three times daily", "Four times daily", "As needed"]
            )
            next_dose_time = st.time_input("Next Dose Time", value=datetime.strptime("08:00", "%H:%M").time())
        
        with col2:
            prescriber = st.text_input("Prescriber", placeholder="e.g., Dr. Smith")
            status = st.selectbox("Status", ["Active", "Inactive", "Completed"], index=0)
            start_date = st.date_input("Start Date", value=datetime.now().date())
            end_date = st.date_input("End Date (Optional)", value=None)
        
        notes = st.text_area("Notes", placeholder="Special instructions or reminders...")
        
        submitted = st.form_submit_button("Add Medicine", use_container_width=True)
        
        if submitted:
            if name and dosage and frequency:
                new_medicine = {
                    "name": name,
                    "dosage": dosage,
                    "frequency": frequency,
                    "next_dose_time": next_dose_time.strftime("%H:%M"),
                    "prescriber": prescriber,
                    "status": status,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d") if end_date else None,
                    "notes": notes,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Try to save to backend first
                client = APIClient()
                client.token = st.session_state.get("auth_token")
                
                resp = client.add_medicine(new_medicine)
                if resp and "id" in resp:
                    new_medicine["id"] = resp["id"]
                
                # Save locally
                if "medicines" not in st.session_state:
                    st.session_state.medicines = []
                st.session_state.medicines.append(new_medicine)
                data_manager.save_medicines(st.session_state.medicines)
                
                st.success(f"✅ {name} added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")


if __name__ == "__main__":
    main()