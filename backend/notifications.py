import os
import firebase_admin
from firebase_admin import credentials, messaging

firebase_initialized = False

def initialize_firebase():
    global firebase_initialized
    if not firebase_initialized:
        try:
            cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                firebase_initialized = True
                print("Firebase initialized successfully")
            else:
                print("Firebase service account file not found")
        except Exception as e:
            print(f"Firebase initialization failed: {str(e)}")

def send_push_notification(device_token: str, title: str, body: str, data: dict = None):
    """
    Send push notification to a device
    
    Args:
        device_token: Firebase device token
        title: Notification title
        body: Notification body
        data: Additional data payload
    """
    if not firebase_initialized:
        initialize_firebase()
    
    if not firebase_initialized:
        return {"success": False, "error": "Firebase not initialized"}
    
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=device_token,
        )
        
        response = messaging.send(message)
        return {"success": True, "message_id": response}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_medicine_reminder(device_token: str, medicine_name: str, dosage: str, time: str):
    """Send medicine reminder notification"""
    return send_push_notification(
        device_token=device_token,
        title="💊 Medicine Reminder",
        body=f"Time to take {medicine_name} - {dosage}",
        data={
            "type": "medicine_reminder",
            "medicine": medicine_name,
            "dosage": dosage,
            "time": time
        }
    )

def send_appointment_reminder(device_token: str, doctor: str, date: str, time: str):
    """Send appointment reminder notification"""
    return send_push_notification(
        device_token=device_token,
        title="📅 Appointment Reminder",
        body=f"You have an appointment with {doctor} on {date} at {time}",
        data={
            "type": "appointment_reminder",
            "doctor": doctor,
            "date": date,
            "time": time
        }
    )
