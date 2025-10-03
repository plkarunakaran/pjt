# pages/6_Emergency_SOS.py - Fixed version
import streamlit as st
from datetime import datetime
import os
import sys

# FIXED: Clean import structure
try:
    from utils.data_manager import DataManager
    from utils.helpers import init_session_state
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from utils.data_manager import DataManager
    from utils.helpers import init_session_state

# FIXED: Import APIClient from root level (not utils)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import APIClient
from utils.theme import apply_theme
st.set_page_config(page_title="Emergency SOS - MedPal", page_icon="🚨", layout="wide")
apply_theme()

def main():
    # Check authentication
    if not st.session_state.get("logged_in"):
        st.error("Please login first")
        st.stop()
    
    # Initialize
    init_session_state()
    data_manager = DataManager()
    
    # Get API client from session or create new one
    client = st.session_state.get("api_client")
    if not client:
        client = APIClient()
        client.token = st.session_state.get("auth_token")
        st.session_state.api_client = client
    
    st.title("🚨 Emergency SOS")
    st.markdown("Quick access to emergency information and contacts")
    st.error("⚠️ **In a real emergency, call 911 (US), 112 (EU), or your local emergency number immediately**")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🆘 Quick Access",
        "📞 Emergency Contacts",
        "🏥 Medical Info",
        "⚙️ Settings"
    ])
    
    with tab1:
        emergency_quick_access(client, data_manager)
    with tab2:
        emergency_contacts_section(data_manager, client)
    with tab3:
        medical_information_section()
    with tab4:
        emergency_settings_section(data_manager)


def emergency_quick_access(client: APIClient, data_manager: DataManager):
    """Emergency quick access section"""
    st.subheader("🆘 Emergency Quick Access")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚨 Emergency Actions")
        
        # Emergency SOS Button
        st.markdown("#### Send Mass Alert")
        sos_message = st.text_area(
            "Emergency Message",
            value="I need immediate help!",
            height=100,
            key="quick_sos_msg"
        )
        
        if st.button("🚨 SEND SOS TO ALL CONTACTS", use_container_width=True, type="primary"):
            with st.spinner("Sending emergency alerts..."):
                resp = client.send_sos(sos_message)
            
            if resp and not resp.get("error"):
                st.success("✅ Emergency alert sent!")
                
                if resp.get("simulation"):
                    st.info("📱 Demo Mode: Configure Twilio in .env for real SMS")
                
                st.write(f"**Contacts Notified:** {resp.get('contacts_notified', 0)}")
                if resp.get("sent_to"):
                    for contact in resp["sent_to"]:
                        st.write(f"✓ {contact}")
            else:
                st.error("Failed to send SOS")
                if resp:
                    st.error(f"Error: {resp.get('error', 'Unknown error')}")

        st.markdown("---")
        
        # Quick dial buttons
        st.markdown("#### Quick Dial")
        
        emergency_contact = get_primary_emergency_contact(data_manager, client)
        if emergency_contact:
            if st.button(
                f"📞 Call {emergency_contact.get('name')}",
                use_container_width=True,
                key="call_primary"
            ):
                st.info(f"Calling: {emergency_contact.get('phone')}")
                log_emergency_action(f"Called {emergency_contact.get('name')}")
        else:
            st.warning("No primary emergency contact set")
        
        if st.button("🏥 Call Emergency Services", use_container_width=True, key="call_emergency"):
            st.error("This would dial emergency services (Demo only)")

    with col2:
        st.markdown("### 📋 Critical Medical Information")
        display_critical_medical_info()
        
        st.markdown("---")
        st.markdown("### 📍 Location Sharing")
        st.info("Location sharing feature coming soon")

    # Activity log
    st.markdown("---")
    st.subheader("📊 Emergency Activity Log")
    display_emergency_logs()


def emergency_contacts_section(data_manager: DataManager, client: APIClient):
    """Emergency contacts management"""
    st.subheader("📞 Emergency Contacts")
    
    # Fetch contacts from API and merge with local
    contacts = []
    try:
        api_contacts = client.get_emergency_contacts()
        if api_contacts and isinstance(api_contacts, list):
            contacts = api_contacts
    except Exception as e:
        st.warning(f"Could not fetch contacts from server: {e}")
    
    # Merge with local contacts
    local_contacts = st.session_state.get("emergency_contacts", [])
    if local_contacts:
        # Add local contacts that don't have IDs (not synced to API)
        for local in local_contacts:
            if 'id' not in local:
                contacts.append(local)
    
    # Store combined list
    st.session_state.emergency_contacts = contacts
    
    # Add new contact form
    with st.expander("➕ Add New Emergency Contact", expanded=False):
        add_emergency_contact_form(data_manager, client)
    
    st.markdown("---")
    
    # Display contacts
    if contacts:
        st.markdown(f"### Saved Contacts ({len(contacts)})")
        
        # Initialize delete confirmation state
        if "delete_contact_confirm" not in st.session_state:
            st.session_state.delete_contact_confirm = None
        
        for i, contact in enumerate(contacts):
            contact_id = contact.get('id', f"local_{i}")
            
            # Check if this contact is awaiting deletion confirmation
            if st.session_state.delete_contact_confirm == contact_id:
                st.warning(f"⚠️ Delete **{contact.get('name')}**? This cannot be undone.")
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("✅ Yes", key=f"confirm_del_{contact_id}"):
                        # Delete from API if has ID
                        if 'id' in contact:
                            resp = client.delete_emergency_contact(contact['id'])
                            if resp and not resp.get("error"):
                                st.success(f"Deleted {contact.get('name')}")
                            else:
                                st.error("Failed to delete from server")
                        # Delete from local state
                        if i < len(st.session_state.get("emergency_contacts", [])):
                            st.session_state.emergency_contacts.pop(i)
                            data_manager.save_emergency_contacts(st.session_state.emergency_contacts)
                        st.session_state.delete_contact_confirm = None
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", key=f"cancel_del_{contact_id}"):
                        st.session_state.delete_contact_confirm = None
                        st.rerun()
                st.markdown("---")
                continue
            
            # Normal display
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    primary_badge = " ⭐ PRIMARY" if contact.get('is_primary') else ""
                    medical_badge = " 🏥 MEDICAL" if contact.get('is_medical') else ""
                    
                    st.markdown(f"**{contact.get('name')}{primary_badge}{medical_badge}**")
                    st.write(f"📞 {contact.get('phone')}")
                    
                    if contact.get("email"):
                        st.write(f"📧 {contact.get('email')}")
                    if contact.get("relationship"):
                        st.caption(f"Relationship: {contact.get('relationship')}")
                    if contact.get("notes"):
                        st.caption(f"💭 {contact.get('notes')}")
                
                with col2:
                    # Call button
                    if st.button("📞 Call", key=f"call_{contact_id}", use_container_width=True):
                        st.info(f"Calling {contact.get('phone')}...")
                        log_emergency_action(f"Called {contact.get('name')}")
                    
                    # SMS button
                    if st.button("💬 SMS", key=f"sms_{contact_id}", use_container_width=True):
                        send_sms_to_contact(client, contact)
                
                with col3:
                    # Delete button
                    if st.button("🗑️", key=f"delete_{contact_id}", use_container_width=True):
                        st.session_state.delete_contact_confirm = contact_id
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No emergency contacts added yet. Add one using the form above.")


def add_emergency_contact_form(data_manager: DataManager, client: APIClient):
    """Form to add new emergency contact"""
    with st.form("add_emergency_contact", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", placeholder="Full name")
            phone = st.text_input("Phone *", placeholder="+1 234 567 8900")
            email = st.text_input("Email", placeholder="email@example.com")
        
        with col2:
            relationship = st.selectbox(
                "Relationship",
                ["Family", "Friend", "Doctor", "Neighbor", "Other"]
            )
            is_primary = st.checkbox("Set as Primary Contact")
            is_medical = st.checkbox("Medical Professional")
        
        address = st.text_input("Address", placeholder="Optional")
        notes = st.text_area("Notes", placeholder="Additional information...")
        
        submitted = st.form_submit_button("Add Contact", use_container_width=True)
        
        if submitted:
            if not name or not phone:
                st.error("Name and phone are required")
                return
            
            new_contact = {
                "name": name,
                "phone": phone,
                "email": email or None,
                "relationship": relationship,
                "is_primary": is_primary,
                "is_medical": is_medical,
                "address": address or None,
                "notes": notes or None
            }
            
            # Try to save to API
            try:
                resp = client.add_emergency_contact(new_contact)
                
                if resp and not resp.get("error") and ("id" in resp or "name" in resp):
                    st.success(f"✅ {name} added successfully!")
                    # Update local state
                    if "emergency_contacts" not in st.session_state:
                        st.session_state.emergency_contacts = []
                    st.session_state.emergency_contacts.append(resp)
                    data_manager.save_emergency_contacts(st.session_state.emergency_contacts)
                    st.rerun()
                else:
                    raise Exception(resp.get("error", "Unknown error") if resp else "No response")
            except Exception as e:
                # Save locally as fallback
                st.warning(f"Could not save to server. Saving locally.")
                if "emergency_contacts" not in st.session_state:
                    st.session_state.emergency_contacts = []
                st.session_state.emergency_contacts.append(new_contact)
                data_manager.save_emergency_contacts(st.session_state.emergency_contacts)
                st.success(f"✅ {name} added locally")
                st.rerun()


def send_sms_to_contact(client: APIClient, contact: dict):
    """Send SMS to a specific contact"""
    message = f"🚨 Emergency alert from {st.session_state.get('username', 'MedPal user')}"
    
    with st.spinner(f"Sending SMS to {contact.get('name')}..."):
        resp = client.send_sms(contact.get('phone'), message)
    
    if resp and not resp.get("error"):
        if resp.get("simulation"):
            st.info("📱 SMS sent (simulation mode)")
        else:
            st.success(f"✅ SMS sent to {contact.get('name')}")
        log_emergency_action(f"Sent SMS to {contact.get('name')}")
    else:
        st.error(f"Failed to send SMS: {resp.get('error', 'Unknown error')}")


def medical_information_section():
    """Display medical information"""
    st.subheader("🏥 Critical Medical Information")
    st.info("This information will be shared with emergency responders")

    # Personal info
    with st.expander("👤 Personal Information", expanded=True):
        display_personal_medical_info()

    # Current medications
    with st.expander("💊 Current Medications", expanded=True):
        medicines = st.session_state.get("medicines", [])
        active = [m for m in medicines if m.get("status") == "Active"]
        
        if active:
            for m in active:
                st.write(f"• **{m.get('name')}** - {m.get('dosage')} ({m.get('frequency')})")
        else:
            st.info("No active medications recorded")

    # Medical conditions
    with st.expander("⚠️ Medical Conditions & Allergies", expanded=True):
        profile = st.session_state.get("medical_profile", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Conditions:**")
            conditions = profile.get("conditions", [])
            if conditions:
                for c in conditions:
                    st.write(f"• {c}")
            else:
                st.info("No conditions recorded")
        
        with col2:
            st.markdown("**Allergies:**")
            allergies = profile.get("allergies", [])
            if allergies:
                for a in allergies:
                    st.error(f"• {a}")
            else:
                st.info("No allergies recorded")


def emergency_settings_section(data_manager: DataManager):
    """Emergency settings and preferences"""
    st.subheader("⚙️ Emergency Settings")

    # Medical profile
    with st.expander("👤 Update Medical Profile", expanded=True):
        update_medical_profile_form(data_manager)

    # Preferences
    with st.expander("🔧 Notification Preferences"):
        auto_notify = st.checkbox(
            "Auto-notify all contacts in emergency",
            value=st.session_state.get("auto_notify_contacts", True)
        )
        
        if st.button("Save Preferences"):
            st.session_state.auto_notify_contacts = auto_notify
            st.success("Preferences saved")


def update_medical_profile_form(data_manager: DataManager):
    """Form to update medical profile"""
    with st.form("medical_profile_form"):
        profile = st.session_state.get("medical_profile", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            blood_types = ["Not specified", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            current_bt = profile.get("blood_type", "Not specified")
            bt_index = blood_types.index(current_bt) if current_bt in blood_types else 0
            blood_type = st.selectbox("Blood Type", blood_types, index=bt_index)
            age = st.number_input("Age", min_value=0, max_value=120, value=profile.get("age", 30))
        
        with col2:
            height = st.text_input("Height", value=profile.get("height", ""), placeholder="e.g., 5'10\"")
            weight = st.text_input("Weight", value=profile.get("weight", ""), placeholder="e.g., 150 lbs")
        
        conditions = st.text_area(
            "Medical Conditions (one per line)",
            value="\n".join(profile.get("conditions", [])),
            height=100
        )
        
        allergies = st.text_area(
            "Allergies (one per line)",
            value="\n".join(profile.get("allergies", [])),
            height=100
        )
        
        submitted = st.form_submit_button("Save Medical Profile", use_container_width=True)
        
        if submitted:
            new_profile = {
                "blood_type": blood_type if blood_type != "Not specified" else None,
                "age": age,
                "height": height,
                "weight": weight,
                "conditions": [c.strip() for c in conditions.splitlines() if c.strip()],
                "allergies": [a.strip() for a in allergies.splitlines() if a.strip()],
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.medical_profile = new_profile
            data_manager.save_medical_profile(new_profile)
            st.success("✅ Medical profile updated")
            st.rerun()


# Helper functions
def display_critical_medical_info():
    """Display critical medical information card"""
    profile = st.session_state.get("medical_profile", {})
    
    if not profile:
        st.warning("No medical profile set. Update in Settings tab.")
        return
    
    with st.container():
        st.markdown("**Essential Info:**")
        
        if profile.get("blood_type"):
            st.write(f"🩸 Blood Type: **{profile['blood_type']}**")
        
        if profile.get("age"):
            st.write(f"👤 Age: {profile['age']}")
        
        if profile.get("conditions"):
            st.warning("⚠️ Conditions: " + ", ".join(profile["conditions"][:3]))
        
        if profile.get("allergies"):
            st.error("🚨 Allergies: " + ", ".join(profile["allergies"][:3]))


def display_personal_medical_info():
    """Display personal medical information"""
    profile = st.session_state.get("medical_profile", {})
    
    if profile:
        col1, col2 = st.columns(2)
        
        with col1:
            if profile.get("age"):
                st.write(f"**Age:** {profile['age']}")
            if profile.get("blood_type"):
                st.write(f"**Blood Type:** {profile['blood_type']}")
        
        with col2:
            if profile.get("height"):
                st.write(f"**Height:** {profile['height']}")
            if profile.get("weight"):
                st.write(f"**Weight:** {profile['weight']}")
    else:
        st.info("No medical profile set")


def get_primary_emergency_contact(data_manager: DataManager, client: APIClient):
    """Get primary emergency contact"""
    # Get contacts from session state
    contacts = st.session_state.get("emergency_contacts", [])
    
    # Find primary
    for c in contacts:
        if c.get("is_primary"):
            return c
    
    # Return first if no primary set
    return contacts[0] if contacts else None


def log_emergency_action(action: str):
    """Log emergency action"""
    if "emergency_logs" not in st.session_state:
        st.session_state.emergency_logs = []
    
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action
    }
    
    st.session_state.emergency_logs.append(log_entry)
    # Keep only last 50 logs
    st.session_state.emergency_logs = st.session_state.emergency_logs[-50:]


def display_emergency_logs():
    """Display emergency activity logs"""
    logs = st.session_state.get("emergency_logs", [])
    
    if logs:
        st.markdown("**Recent Activity:**")
        for log in reversed(logs[-10:]):  # Show last 10
            st.text(f"{log['timestamp']}: {log['action']}")
    else:
        st.info("No emergency activity recorded")


if __name__ == "__main__":
    main()