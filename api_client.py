import requests
from typing import Optional, Dict, List
import streamlit as st

# FIXED: Consistent API URL
API_URL = "http://127.0.0.1:8000/api"

class APIClient:
    def __init__(self):
        self.token = None
        self.timeout = 10  # ADDED: Request timeout

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """
        Centralized request handler with error handling
        ADDED: Better error handling and timeout
        """
        try:
            url = f"{API_URL}{endpoint}"
            kwargs['timeout'] = self.timeout
            
            response = requests.request(method, url, **kwargs)
            
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                st.error("❌ Session expired. Please login again.")
                return {"error": "Unauthorized"}
            elif response.status_code == 404:
                return {"error": "Not found"}
            else:
                return {"error": response.text}
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timeout. Please check your connection.")
            return {"error": "Timeout"}
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to server. Is the backend running?")
            return {"error": "Connection failed"}
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return {"error": str(e)}

    def get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    # ==================== AUTH ====================
    def signup(self, username: str, email: str, password: str, full_name: str) -> Optional[Dict]:
        """Register a new user"""
        return self._make_request(
            "POST",
            "/signup",
            json={
                "username": username,
                "email": email,
                "password": password,
                "full_name": full_name
            }
        )

    def login(self, username: str, password: str) -> bool:
        """Login and store access token"""
        response = self._make_request(
            "POST",
            "/login",
            data={
                "username": username,
                "password": password
            }
        )
        
        if response and "access_token" in response:
            self.token = response["access_token"]
            # FIXED: Store token consistently in session state
            st.session_state.auth_token = self.token
            return True
        return False

    # ==================== MEDICINES ====================
    def get_medicines(self) -> List[Dict]:
        """Get all medicines for current user"""
        result = self._make_request("GET", "/medicines", headers=self.get_headers())
        return result if isinstance(result, list) else []

    def add_medicine(self, medicine_data: Dict) -> Optional[Dict]:
        """Add a new medicine"""
        return self._make_request(
            "POST",
            "/medicines",
            json=medicine_data,
            headers=self.get_headers()
        )

    def delete_medicine(self, medicine_id: int) -> Optional[Dict]:
        """Delete a medicine"""
        return self._make_request(
            "DELETE",
            f"/medicines/{medicine_id}",
            headers=self.get_headers()
        )

    def update_medicine(self, medicine_id: int, medicine_data: Dict) -> Optional[Dict]:
        """Update a medicine"""
        return self._make_request(
            "PUT",
            f"/medicines/{medicine_id}",
            json=medicine_data,
            headers=self.get_headers()
        )

    # ==================== APPOINTMENTS ====================
    def get_appointments(self) -> List[Dict]:
        """Get all appointments for current user"""
        result = self._make_request("GET", "/appointments", headers=self.get_headers())
        return result if isinstance(result, list) else []

    def add_appointment(self, appointment_data: Dict) -> Optional[Dict]:
        """Add a new appointment"""
        return self._make_request(
            "POST",
            "/appointments",
            json=appointment_data,
            headers=self.get_headers()
        )

    def delete_appointment(self, appointment_id: int) -> Optional[Dict]:
        """Delete an appointment"""
        return self._make_request(
            "DELETE",
            f"/appointments/{appointment_id}",
            headers=self.get_headers()
        )

    def update_appointment(self, appointment_id: int, appointment_data: Dict) -> Optional[Dict]:
        """Update an appointment"""
        return self._make_request(
            "PUT",
            f"/appointments/{appointment_id}",
            json=appointment_data,
            headers=self.get_headers()
        )

    # ==================== HEALTH METRICS ====================
    def get_health_metrics(self) -> List[Dict]:
        """Get all health metrics for current user"""
        result = self._make_request("GET", "/health_metrics", headers=self.get_headers())
        return result if isinstance(result, list) else []

    def add_health_metric(self, metric_data: Dict) -> Optional[Dict]:
        """Add a new health metric"""
        return self._make_request(
            "POST",
            "/health_metrics",
            json=metric_data,
            headers=self.get_headers()
        )

    # ==================== EMERGENCY CONTACTS ====================
    def get_emergency_contacts(self) -> List[Dict]:
        """Get emergency contacts"""
        result = self._make_request("GET", "/emergency_contacts", headers=self.get_headers())
        return result if isinstance(result, list) else []

    def add_emergency_contact(self, contact_data: Dict) -> Optional[Dict]:
        """Add emergency contact"""
        return self._make_request(
            "POST",
            "/emergency_contacts",
            json=contact_data,
            headers=self.get_headers()
        )

    def delete_emergency_contact(self, contact_id: int) -> Optional[Dict]:
        """Delete emergency contact"""
        return self._make_request(
            "DELETE",
            f"/emergency_contacts/{contact_id}",
            headers=self.get_headers()
        )

    # ==================== SOS ====================
    def send_sos(self, message: str) -> Optional[Dict]:
        """Send emergency SOS"""
        return self._make_request(
            "POST",
            "/sos",
            json={"message": message},
            headers=self.get_headers()
        )

    def send_sms(self, to: str, message: str) -> Optional[Dict]:
        """Send SMS via Twilio"""
        return self._make_request(
            "POST",
            "/send-sms",
            json={"to": to, "message": message},
            headers=self.get_headers()
        )

    # ==================== UTILITY ====================
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.token is not None

    def logout(self):
        """Clear authentication token"""
        self.token = None
        if "auth_token" in st.session_state:
            del st.session_state.auth_token