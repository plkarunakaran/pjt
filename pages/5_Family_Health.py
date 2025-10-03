import streamlit as st
from datetime import datetime
from utils.data_manager import DataManager
from utils.helpers import init_session_state
from utils.theme import apply_theme

st.set_page_config(page_title="Family Health - MedPal", page_icon="👨‍👩‍👧‍👦")
apply_theme()

def main():
    """Main entry point for Family Health page."""
    init_session_state()
    data_manager = DataManager()

    st.title("👨‍👩‍👧‍👦 Family Health")
    st.markdown("Manage health profiles for your family members")

    # Tabs for viewing and adding members
    tab1, tab2 = st.tabs(["👥 Family Members", "➕ Add Member"])

    with tab1:
        display_family_members()

    with tab2:
        add_family_member_form()


def display_family_members():
    """Display all family members and their health profiles."""
    family_members = st.session_state.get("family_members", [])

    if not family_members:
        st.info("No family members added yet. Use the 'Add Member' tab to start creating profiles.")
        return

    # Search + filter
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search family members", placeholder="Enter name...")
    with col2:
        relationship_filter = st.selectbox(
            "Filter by Relationship",
            ["All"] + sorted(set(m.get("relationship", "") for m in family_members if m.get("relationship")))
        )

    # Apply filters
    filtered_members = family_members
    if search_term:
        search_lower = search_term.lower()
        filtered_members = [m for m in filtered_members if search_lower in m.get("name", "").lower()]

    if relationship_filter != "All":
        filtered_members = [m for m in filtered_members if m.get("relationship") == relationship_filter]

    st.markdown(f"**Showing {len(filtered_members)} family member(s)**")

    # Initialize delete confirmation state
    if "delete_confirm_index" not in st.session_state:
        st.session_state.delete_confirm_index = None

    # Display member cards
    for i, member in enumerate(filtered_members):
        # Get the actual index in the original list
        original_index = family_members.index(member)
        
        with st.container():
            # Check if this member is awaiting delete confirmation
            if st.session_state.delete_confirm_index == original_index:
                st.warning(f"⚠️ Are you sure you want to delete **{member.get('name', 'Unknown')}**? This action cannot be undone.")
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("✅ Yes, Delete", key=f"confirm_delete_{original_index}"):
                        member_name = member.get("name", "Unknown")
                        del st.session_state.family_members[original_index]
                        DataManager().save_family_members(st.session_state.family_members)
                        st.session_state.delete_confirm_index = None
                        st.success(f"✅ {member_name} has been deleted.")
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", key=f"cancel_delete_{original_index}"):
                        st.session_state.delete_confirm_index = None
                        st.rerun()
            else:
                # Normal display
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.subheader(f"👤 {member.get('name', 'Unknown')}")
                    st.write(f"**Relationship:** {member.get('relationship', 'Unknown')}")
                    if member.get("age"):
                        st.write(f"**Age:** {member.get('age')} years")
                    if member.get("blood_type"):
                        st.write(f"**Blood Type:** {member.get('blood_type')}")

                with col2:
                    if st.button("📋 View Profile", key=f"view_{original_index}"):
                        st.session_state.view_profile_index = original_index
                        st.rerun()

                with col3:
                    if st.button("✏️ Edit", key=f"edit_{original_index}"):
                        st.session_state.edit_member_index = original_index
                        st.rerun()

                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{original_index}"):
                        st.session_state.delete_confirm_index = original_index
                        st.rerun()

                # Quick health summary
                st.markdown("**📊 Health Summary:**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Medicines", len(member.get("medicines", [])))
                with col2:
                    st.metric("Appointments", len(member.get("appointments", [])))
                with col3:
                    st.metric("Conditions", len(member.get("medical_conditions", [])))
                with col4:
                    st.metric("Allergies", len(member.get("allergies", [])))

            st.markdown("---")

    # Handle view profile
    if "view_profile_index" in st.session_state and st.session_state.view_profile_index is not None:
        if st.session_state.view_profile_index < len(family_members):
            view_member_profile(family_members[st.session_state.view_profile_index])
            if st.button("← Back to List", key="back_from_view"):
                st.session_state.view_profile_index = None
                st.rerun()

    # Handle edit member
    if "edit_member_index" in st.session_state and st.session_state.edit_member_index is not None:
        if st.session_state.edit_member_index < len(family_members):
            edit_family_member(st.session_state.edit_member_index, family_members[st.session_state.edit_member_index])


def view_member_profile(member):
    """Detailed profile for a family member."""
    st.subheader(f"👤 {member.get('name', 'Unknown')} - Health Profile")

    # Basic Info
    with st.expander("👤 Basic Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {member.get('name', 'Not specified')}")
            st.write(f"**Relationship:** {member.get('relationship', 'Not specified')}")
            st.write(f"**Age:** {member.get('age', 'Not specified')}")
            st.write(f"**Gender:** {member.get('gender', 'Not specified')}")
        with col2:
            st.write(f"**Blood Type:** {member.get('blood_type', 'Not specified')}")
            st.write(f"**Date of Birth:** {member.get('date_of_birth', 'Not specified')}")
            st.write(f"**Phone:** {member.get('phone', 'Not specified')}")
            st.write(f"**Emergency Contact:** {member.get('emergency_contact', 'Not specified')}")

    # Medical Conditions
    with st.expander("🏥 Medical Conditions"):
        conditions = member.get("medical_conditions", [])
        if conditions:
            for idx, condition in enumerate(conditions):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• {condition}")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_condition_{idx}_{member['name']}"):
                        conditions.pop(idx)
                        DataManager().save_family_members(st.session_state.family_members)
                        st.success("Condition deleted!")
                        st.rerun()
        else:
            st.info("No medical conditions recorded.")

    # Allergies
    with st.expander("⚠️ Allergies"):
        allergies = member.get("allergies", [])
        if allergies:
            for idx, allergy in enumerate(allergies):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• {allergy}")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_allergy_{idx}_{member['name']}"):
                        allergies.pop(idx)
                        DataManager().save_family_members(st.session_state.family_members)
                        st.success("Allergy deleted!")
                        st.rerun()
        else:
            st.info("No allergies recorded.")

    # Medicines
    with st.expander("💊 Current Medicines"):
        medicines = member.get("medicines", [])
        if medicines:
            for idx, med in enumerate(medicines):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• **{med.get('name', 'Unknown')}** - {med.get('dosage', 'N/A')}, {med.get('frequency', 'N/A')}")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_med_{idx}_{member['name']}"):
                        medicines.pop(idx)
                        DataManager().save_family_members(st.session_state.family_members)
                        st.success("Medicine deleted!")
                        st.rerun()
        else:
            st.info("No medicines recorded.")

    # Appointments
    with st.expander("📅 Recent Appointments"):
        appointments = member.get("appointments", [])
        if appointments:
            for idx, appt in enumerate(appointments):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"• **{appt.get('doctor', 'Unknown')}** - {appt.get('date', 'Unknown')}")
                    if appt.get("reason"):
                        st.write(f"  Reason: {appt['reason']}")
                with col2:
                    if st.button("🗑️ Delete", key=f"del_appt_{idx}_{member['name']}"):
                        appointments.pop(idx)
                        DataManager().save_family_members(st.session_state.family_members)
                        st.success("Appointment deleted!")
                        st.rerun()
        else:
            st.info("No appointments recorded.")

    # Insurance
    with st.expander("🛡️ Insurance Information"):
        insurance = member.get("insurance", {})
        if insurance:
            st.write(f"**Provider:** {insurance.get('provider', 'Not specified')}")
            st.write(f"**Policy Number:** {insurance.get('policy_number', 'Not specified')}")
            st.write(f"**Group Number:** {insurance.get('group_number', 'Not specified')}")
        else:
            st.info("No insurance information recorded.")


def add_family_member_form():
    """Form to add a new family member."""
    st.subheader("Add Family Member")

    with st.form("add_family_member_form"):
        # Basic Info
        st.markdown("**👤 Basic Information**")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name *", placeholder="e.g., John Smith")
            relationship = st.selectbox(
                "Relationship *",
                ["Spouse/Partner", "Child", "Parent", "Sibling", "Grandparent", "Grandchild", "Other"]
            )
            age = st.number_input("Age", min_value=0, max_value=150, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])

        with col2:
            date_of_birth = st.date_input("Date of Birth")
            blood_type = st.selectbox(
                "Blood Type",
                ["Not specified", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            )
            phone = st.text_input("Phone Number", placeholder="e.g., +1 234 567 8900")
            emergency_contact = st.text_input("Emergency Contact", placeholder="Name and phone number")

        # Medical Info
        st.markdown("---")
        st.markdown("**🏥 Medical Information**")
        medical_conditions = st.text_area(
            "Medical Conditions",
            placeholder="Enter each condition on a new line"
        )
        allergies = st.text_area(
            "Allergies",
            placeholder="Enter each allergy on a new line"
        )

        # Insurance Info
        st.markdown("---")
        st.markdown("**🛡️ Insurance Information**")
        col1, col2 = st.columns(2)
        with col1:
            insurance_provider = st.text_input("Insurance Provider")
            policy_number = st.text_input("Policy Number")
        with col2:
            group_number = st.text_input("Group Number")
            insurance_phone = st.text_input("Insurance Phone")

        notes = st.text_area("Additional Notes")

        submitted = st.form_submit_button("Add Family Member", use_container_width=True)
        if submitted:
            if name and relationship:
                new_member = {
                    "name": name,
                    "relationship": relationship,
                    "age": age,
                    "gender": gender,
                    "date_of_birth": date_of_birth.strftime("%Y-%m-%d") if date_of_birth else None,
                    "blood_type": blood_type if blood_type != "Not specified" else None,
                    "phone": phone,
                    "emergency_contact": emergency_contact,
                    "medical_conditions": [c.strip() for c in medical_conditions.split("\n") if c.strip()],
                    "allergies": [a.strip() for a in allergies.split("\n") if a.strip()],
                    "insurance": {
                        "provider": insurance_provider,
                        "policy_number": policy_number,
                        "group_number": group_number,
                        "phone": insurance_phone,
                    } if insurance_provider else {},
                    "medicines": [],
                    "appointments": [],
                    "notes": notes,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                if "family_members" not in st.session_state:
                    st.session_state.family_members = []
                st.session_state.family_members.append(new_member)

                DataManager().save_family_members(st.session_state.family_members)
                st.success(f"✅ {name} has been added!")
                st.rerun()
            else:
                st.error("Please fill in required fields (*).")


def edit_family_member(index, member):
    """Edit a family member."""
    st.subheader(f"Edit: {member.get('name', 'Unknown')}")

    with st.form(f"edit_member_form_{index}"):
        # Basic Info
        st.markdown("**👤 Basic Information**")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name *", value=member.get("name", ""))
            relationships = ["Spouse/Partner", "Child", "Parent", "Sibling", "Grandparent", "Grandchild", "Other"]
            current_rel = member.get("relationship", "Other")
            rel_index = relationships.index(current_rel) if current_rel in relationships else 0
            relationship = st.selectbox("Relationship *", relationships, index=rel_index)
            age = st.number_input("Age", min_value=0, max_value=150, value=member.get("age", 25))
            genders = ["Male", "Female", "Other", "Prefer not to say"]
            current_gender = member.get("gender", "Male")
            gender_index = genders.index(current_gender) if current_gender in genders else 0
            gender = st.selectbox("Gender", genders, index=gender_index)

        with col2:
            dob_value = None
            if member.get("date_of_birth"):
                try:
                    dob_value = datetime.strptime(member["date_of_birth"], "%Y-%m-%d").date()
                except Exception:
                    pass
            date_of_birth = st.date_input("Date of Birth", value=dob_value)
            blood_types = ["Not specified", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            current_bt = member.get("blood_type", "Not specified")
            bt_index = blood_types.index(current_bt) if current_bt in blood_types else 0
            blood_type = st.selectbox("Blood Type", blood_types, index=bt_index)
            phone = st.text_input("Phone Number", value=member.get("phone", ""))
            emergency_contact = st.text_input("Emergency Contact", value=member.get("emergency_contact", ""))

        # Medical Info
        st.markdown("---")
        st.markdown("**🏥 Medical Information**")
        medical_conditions = st.text_area("Medical Conditions", value="\n".join(member.get("medical_conditions", [])))
        allergies = st.text_area("Allergies", value="\n".join(member.get("allergies", [])))

        # Insurance Info
        st.markdown("---")
        st.markdown("**🛡️ Insurance Information**")
        insurance = member.get("insurance", {})
        col1, col2 = st.columns(2)
        with col1:
            insurance_provider = st.text_input("Insurance Provider", value=insurance.get("provider", ""))
            policy_number = st.text_input("Policy Number", value=insurance.get("policy_number", ""))
        with col2:
            group_number = st.text_input("Group Number", value=insurance.get("group_number", ""))
            insurance_phone = st.text_input("Insurance Phone", value=insurance.get("phone", ""))

        notes = st.text_area("Additional Notes", value=member.get("notes", ""))

        col1, col2 = st.columns(2)
        with col1:
            update = st.form_submit_button("Update Member", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        if update:
            if name and relationship:
                updated_member = {
                    **member,
                    "name": name,
                    "relationship": relationship,
                    "age": age,
                    "gender": gender,
                    "date_of_birth": date_of_birth.strftime("%Y-%m-%d") if date_of_birth else None,
                    "blood_type": blood_type if blood_type != "Not specified" else None,
                    "phone": phone,
                    "emergency_contact": emergency_contact,
                    "medical_conditions": [c.strip() for c in medical_conditions.split("\n") if c.strip()],
                    "allergies": [a.strip() for a in allergies.split("\n") if a.strip()],
                    "insurance": {
                        "provider": insurance_provider,
                        "policy_number": policy_number,
                        "group_number": group_number,
                        "phone": insurance_phone,
                    } if insurance_provider else {},
                    "notes": notes,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.session_state.family_members[index] = updated_member
                DataManager().save_family_members(st.session_state.family_members)
                st.session_state.edit_member_index = None
                st.success(f"✅ {name}'s profile has been updated!")
                st.rerun()
            else:
                st.error("Please fill in required fields (*)")

        if cancel:
            st.session_state.edit_member_index = None
            st.rerun()


if __name__ == "__main__":
    main()