import json
import os
from datetime import datetime
import streamlit as st
import requests


class DataManager:
    """Handles data persistence for the MedPal application.
       Works in both local JSON mode and API backend mode.
    """

    def __init__(self, use_api=False, api_url="http://127.0.0.1:8000"):
        self.data_dir = "data"
        self.use_api = use_api
        self.api_url = api_url.rstrip("/")  # remove trailing slash

        if not self.use_api:
            self.ensure_data_directory()

    # -----------------------
    # Helpers
    # -----------------------
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_file_path(self, filename):
        return os.path.join(self.data_dir, filename)

    def _api_get(self, endpoint):
        try:
            res = requests.get(f"{self.api_url}{endpoint}")
            res.raise_for_status()
            return res.json()
        except Exception as e:
            st.error(f"API GET error {endpoint}: {str(e)}")
            return []

    def _api_post(self, endpoint, data):
        try:
            res = requests.post(f"{self.api_url}{endpoint}", json=data)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            st.error(f"API POST error {endpoint}: {str(e)}")
            return None

    def _api_put(self, endpoint, data):
        try:
            res = requests.put(f"{self.api_url}{endpoint}", json=data)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            st.error(f"API PUT error {endpoint}: {str(e)}")
            return None

    def _api_delete(self, endpoint):
        try:
            res = requests.delete(f"{self.api_url}{endpoint}")
            res.raise_for_status()
            return res.json()
        except Exception as e:
            st.error(f"API DELETE error {endpoint}: {str(e)}")
            return None

    # -----------------------
    # Medicines
    # -----------------------
    def save_medicines(self, medicines):
        if self.use_api:
            return self._api_post("/medicines/", medicines)
        try:
            with open(self._get_file_path("medicines.json"), "w") as f:
                json.dump(medicines, f, indent=2)
        except Exception as e:
            st.error(f"Error saving medicines: {str(e)}")

    def load_medicines(self):
        if self.use_api:
            return self._api_get("/medicines/")
        try:
            path = self._get_file_path("medicines.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading medicines: {str(e)}")
        return []

    # -----------------------
    # Appointments
    # -----------------------
    def save_appointments(self, appointments):
        if self.use_api:
            return self._api_post("/appointments/", appointments)
        try:
            with open(self._get_file_path("appointments.json"), "w") as f:
                json.dump(appointments, f, indent=2)
        except Exception as e:
            st.error(f"Error saving appointments: {str(e)}")

    def load_appointments(self):
        if self.use_api:
            return self._api_get("/appointments/")
        try:
            path = self._get_file_path("appointments.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading appointments: {str(e)}")
        return []

    # -----------------------
    # Health Metrics
    # -----------------------
    def save_health_metrics(self, health_metrics):
        if self.use_api:
            return self._api_post("/health-metrics/", health_metrics)
        try:
            with open(self._get_file_path("health_metrics.json"), "w") as f:
                json.dump(health_metrics, f, indent=2)
        except Exception as e:
            st.error(f"Error saving health metrics: {str(e)}")

    def load_health_metrics(self):
        if self.use_api:
            return self._api_get("/health-metrics/")
        try:
            path = self._get_file_path("health_metrics.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading health metrics: {str(e)}")
        return []

    # -----------------------
    # Family Members
    # -----------------------
    def save_family_members(self, family_members):
        if self.use_api:
            return self._api_post("/family-members/", family_members)
        try:
            with open(self._get_file_path("family_members.json"), "w") as f:
                json.dump(family_members, f, indent=2)
        except Exception as e:
            st.error(f"Error saving family members: {str(e)}")

    def load_family_members(self):
        if self.use_api:
            return self._api_get("/family-members/")
        try:
            path = self._get_file_path("family_members.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading family members: {str(e)}")
        return []

    # -----------------------
    # Emergency Contacts
    # -----------------------
    def save_emergency_contacts(self, emergency_contacts):
        if self.use_api:
            return self._api_post("/emergency-contacts/", emergency_contacts)
        try:
            with open(self._get_file_path("emergency_contacts.json"), "w") as f:
                json.dump(emergency_contacts, f, indent=2)
        except Exception as e:
            st.error(f"Error saving emergency contacts: {str(e)}")

    def load_emergency_contacts(self):
        if self.use_api:
            return self._api_get("/emergency-contacts/")
        try:
            path = self._get_file_path("emergency_contacts.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading emergency contacts: {str(e)}")
        return []

    # -----------------------
    # Medical Profile
    # -----------------------
    def save_medical_profile(self, medical_profile):
        if self.use_api:
            return self._api_post("/medical-profile/", medical_profile)
        try:
            with open(self._get_file_path("medical_profile.json"), "w") as f:
                json.dump(medical_profile, f, indent=2)
        except Exception as e:
            st.error(f"Error saving medical profile: {str(e)}")

    def load_medical_profile(self):
        if self.use_api:
            return self._api_get("/medical-profile/")
        try:
            path = self._get_file_path("medical_profile.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading medical profile: {str(e)}")
        return {}

    # -----------------------
    # User Preferences
    # -----------------------
    def save_user_preferences(self, preferences):
        if self.use_api:
            return self._api_post("/user-preferences/", preferences)
        try:
            with open(self._get_file_path("user_preferences.json"), "w") as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            st.error(f"Error saving user preferences: {str(e)}")

    def load_user_preferences(self):
        if self.use_api:
            return self._api_get("/user-preferences/")
        try:
            path = self._get_file_path("user_preferences.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading user preferences: {str(e)}")
        return {}

    # -----------------------
    # Utilities (backup, restore, export, stats)
    # -----------------------
    def backup_data(self):
        if self.use_api:
            st.warning("Backup not implemented for API mode")
            return None
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.data_dir, f"backup_{timestamp}")
            os.makedirs(backup_dir, exist_ok=True)
            for file_name in os.listdir(self.data_dir):
                if file_name.endswith(".json"):
                    with open(self._get_file_path(file_name), "r") as src:
                        data = json.load(src)
                    with open(os.path.join(backup_dir, file_name), "w") as dst:
                        json.dump(data, dst, indent=2)
            return backup_dir
        except Exception as e:
            st.error(f"Error creating backup: {str(e)}")
            return None

    def get_data_statistics(self):
        if self.use_api:
            return {"api_mode": True}
        try:
            return {
                "medicines_count": len(self.load_medicines()),
                "appointments_count": len(self.load_appointments()),
                "health_metrics_count": len(self.load_health_metrics()),
                "family_members_count": len(self.load_family_members()),
                "emergency_contacts_count": len(self.load_emergency_contacts()),
                "has_medical_profile": bool(self.load_medical_profile()),
                "data_size_mb": self.get_data_size(),
            }
        except Exception as e:
            st.error(f"Error getting data statistics: {str(e)}")
            return {}

    def get_data_size(self):
        try:
            total_size = 0
            for file_name in os.listdir(self.data_dir):
                if file_name.endswith(".json"):
                    total_size += os.path.getsize(self._get_file_path(file_name))
            return round(total_size / (1024 * 1024), 2)
        except Exception:
            return 0
