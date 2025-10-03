# MedPal API Documentation

## Base URL
```
http://your-backend-url:8000
```

## Authentication
All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Endpoints

### Authentication

#### POST /api/signup
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response:** User object

#### POST /api/login
Login and get access token.

**Request Body (form data):**
```
username: johndoe
password: securepassword
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### GET /api/me
Get current user information (requires authentication).

**Response:** User object

### Medicines

#### POST /api/medicines
Add a new medicine (requires authentication).

**Request Body:**
```json
{
  "name": "Paracetamol",
  "dosage": "500mg",
  "frequency": "Twice a day",
  "time_of_day": "8:00 AM, 8:00 PM",
  "start_date": "2025-10-01",
  "end_date": "2025-10-15",
  "prescriber": "Dr. Smith",
  "notes": "Take with food",
  "status": "Active"
}
```

#### GET /api/medicines
Get all medicines for current user (requires authentication).

**Response:** Array of medicine objects

#### DELETE /api/medicines/{medicine_id}
Delete a medicine (requires authentication).

### Appointments

#### POST /api/appointments
Add a new appointment (requires authentication).

**Request Body:**
```json
{
  "doctor": "Dr. Smith",
  "specialty": "Cardiologist",
  "date": "2025-10-15",
  "time": "10:00 AM",
  "location": "City Hospital",
  "reason": "Regular checkup",
  "notes": "Bring previous reports",
  "reminder_enabled": true,
  "status": "Scheduled"
}
```

#### GET /api/appointments
Get all appointments for current user (requires authentication).

#### DELETE /api/appointments/{appointment_id}
Delete an appointment (requires authentication).

### Health Metrics

#### POST /api/health_metrics
Add a health metric (requires authentication).

**Request Body:**
```json
{
  "metric_type": "Blood Pressure",
  "value": 120.0,
  "unit": "mmHg",
  "notes": "Feeling good",
  "source": "Manual"
}
```

#### GET /api/health_metrics
Get all health metrics for current user (requires authentication).

### Emergency Contacts

#### POST /api/emergency_contacts
Add an emergency contact (requires authentication).

**Request Body:**
```json
{
  "name": "Jane Doe",
  "contact_relationship": "Spouse",
  "phone": "+1234567890",
  "email": "jane@example.com",
  "is_primary": true
}
```

#### GET /api/emergency_contacts
Get all emergency contacts for current user (requires authentication).

### SOS

#### POST /api/sos
Send emergency SMS to all emergency contacts (requires authentication).

**Request Body:**
```json
{
  "message": "Emergency! I need help."
}
```

**Response:**
```json
{
  "message": "SOS sent successfully",
  "sent_to": ["Jane Doe", "John Smith"],
  "contacts_notified": 2
}
```

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing authentication token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
