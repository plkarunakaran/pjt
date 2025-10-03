# MedPal - Your Health Companion

## Overview

MedPal is a comprehensive mobile health management application with a dual-tier architecture: a Streamlit MVP for rapid prototyping and a production-ready FastAPI backend with Flutter mobile app for Android/iOS deployment. The system includes user authentication, PostgreSQL database, Firebase push notifications for medication reminders, and Twilio integration for emergency SOS functionality.

**Core Purpose**: Enable users to manage their personal health information via a native mobile application with secure cloud-based data persistence, real-time notifications, and emergency contact features.

**Key Capabilities**:
- User authentication with JWT tokens
- Medicine tracking with dosage schedules and push notifications
- Appointment scheduling with reminders
- Health metrics monitoring (blood pressure, weight, heart rate, blood sugar)
- Emergency SOS via SMS to emergency contacts
- Multi-user support with secure data isolation
- Native mobile apps for iOS and Android

## Recent Changes (October 2025)

### Major Architecture Migration
- **Database Migration**: Migrated from JSON file storage to PostgreSQL for scalability and multi-user support
- **Backend API**: Built complete FastAPI backend with RESTful endpoints and JWT authentication
- **Mobile App**: Created Flutter application structure with authentication, API integration, and core screens
- **Twilio Integration**: Implemented emergency SOS feature using Replit's Twilio connector
- **Firebase Setup**: Added Firebase Admin SDK for push notification infrastructure
- **Dual-Tier System**: Maintained Streamlit app as MVP/prototype tool alongside production backend

### Technical Fixes
- Renamed `EmergencyContact.relationship` to `contact_relationship` to avoid SQLAlchemy conflict
- Added email-validator dependency for Pydantic email validation
- Configured both workflows: Backend API (port 8000) and Streamlit (port 5000)
- Created comprehensive API documentation and setup instructions

## User Preferences

Preferred communication style: Simple, everyday language.
Development approach: Production-ready architecture with security best practices.

## System Architecture

### Two-Tier Architecture

```
Prototype Tier (MVP):
┌─────────────────┐
│  Streamlit App  │ (Port 5000) - Rapid prototyping & testing
└─────────────────┘

Production Tier:
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Flutter App    │────▶│  FastAPI     │────▶│  PostgreSQL  │
│  iOS + Android  │     │  Backend     │     │  Database    │
└─────────────────┘     │  (Port 8000) │     └──────────────┘
                        └──────────────┘
                               │
                               ├─────▶ Twilio (Emergency SOS)
                               │
                               └─────▶ Firebase (Push Notifications)
```

### Backend Architecture (FastAPI)

**Framework**: FastAPI with async support
- **Entry Point**: `backend/main.py` - FastAPI application with CORS middleware
- **Database ORM**: SQLAlchemy with async session support
- **Authentication**: JWT token-based auth with bcrypt password hashing
- **API Structure**: RESTful endpoints with Pydantic schema validation

**Core Modules**:
- `backend/models.py`: SQLAlchemy ORM models (User, Medicine, Appointment, HealthMetric, EmergencyContact)
- `backend/schemas.py`: Pydantic schemas for request/response validation
- `backend/auth.py`: JWT token generation, password hashing, user authentication
- `backend/database.py`: Database session management and connection pooling
- `backend/notifications.py`: Firebase Cloud Messaging integration for push notifications

**Database Models**:
- `users`: User accounts with hashed passwords
- `medicines`: Medicine records with relationships to users
- `appointments`: Medical appointments with reminder settings
- `health_metrics`: Health measurements with timestamps
- `emergency_contacts`: Emergency contact information (renamed relationship field to `contact_relationship`)

**API Endpoints** (see API_DOCUMENTATION.md):
- Authentication: `/api/signup`, `/api/login`, `/api/me`
- Medicines: `/api/medicines` (GET, POST, DELETE)
- Appointments: `/api/appointments` (GET, POST, DELETE)
- Health Metrics: `/api/health_metrics` (GET, POST)
- Emergency Contacts: `/api/emergency_contacts` (GET, POST)
- SOS: `/api/sos` (POST) - Twilio SMS integration

### Frontend Architecture (Flutter Mobile)

**Framework**: Flutter with Material Design
- **Structure**: `flutter_app/lib/` with organized services and screens
- **State Management**: Provider pattern (planned) with local state
- **API Integration**: Centralized `ApiService` class for all backend communication

**Core Components**:
- `lib/main.dart`: App entry point with routing
- `lib/services/auth_service.dart`: JWT token storage and authentication state
- `lib/services/api_service.dart`: HTTP client for backend API calls
- `lib/screens/`: Login, Home, Medicines, Appointments, Health Metrics, SOS screens

**Platform Support**:
- Android: Minimum SDK 21, compiled with SDK 34
- iOS: Minimum iOS 12.0, compiled with latest

### Streamlit MVP (Port 5000)

**Framework**: Streamlit multi-page application
- **Purpose**: Rapid prototyping, testing, and admin interface
- **Entry Point**: `app.py` serves as the landing page
- **Architecture**: Same as production but uses session state for demo/testing

**UI Components**:
- Tab-based interfaces for organizing functionality
- Card-based metric displays using `st.metric()`
- Form-based data entry with validation
- Interactive charts for health metrics

### Database Architecture (PostgreSQL)

**Connection**: Replit managed PostgreSQL via `DATABASE_URL` environment variable

**Schema Management**:
- SQLAlchemy ORM handles table creation automatically
- Models defined in `backend/models.py`
- Foreign key relationships between users and their data
- Automatic timestamps with `DateTime` fields

**Data Isolation**:
- All user data scoped by `user_id` foreign key
- JWT authentication ensures users only access their own data
- Proper indexing on frequently queried fields

### Integration Architecture

**Twilio (Emergency SOS)**:
- Integration ID: `conn_twilio_01K6FJA0XK274C1X0NVGR7AQ0G`
- Managed via Replit connector for secure credential handling
- Sends SMS to all emergency contacts on SOS trigger
- Endpoint: `POST /api/sos`

**Firebase (Push Notifications)**:
- Firebase Admin SDK configured in `backend/notifications.py`
- Credentials stored in `firebase-credentials.json`
- FCM tokens stored per user for targeted notifications
- Notification scheduler for medication/appointment reminders

### Security Architecture

**Authentication Flow**:
1. User registers via `/api/signup` → password hashed with bcrypt
2. User logs in via `/api/login` → JWT token issued (24h expiry)
3. Client stores token and includes in Authorization header
4. Backend validates token on protected endpoints via dependency injection

**Security Measures**:
- Password hashing with bcrypt (12 rounds)
- JWT tokens with HS256 algorithm and secret key
- Environment variables for sensitive credentials
- CORS middleware configured for production domains
- Input validation with Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM

### Data Flow Pattern

**Mobile App Flow**:
1. **Authentication**: User logs in → JWT token stored in `AuthService`
2. **API Requests**: `ApiService` includes token in all requests
3. **Data Sync**: API responses update local Flutter state
4. **Push Notifications**: Firebase sends reminders → app displays notification
5. **SOS Flow**: User triggers SOS → backend sends Twilio SMS → contacts notified

**Streamlit Flow** (MVP):
1. **Session State**: Data loaded from backend API or local demo data
2. **User Actions**: Forms submitted → API calls to backend
3. **Updates**: Response updates session state → UI refreshes

### Error Handling

**Backend**:
- HTTPException for API errors with appropriate status codes
- Database connection error handling with retries
- Validation errors caught by Pydantic and returned as 400 errors
- Logging for debugging (uvicorn access logs)

**Frontend**:
- Try-catch blocks around API calls
- User-friendly error messages displayed in UI
- Token refresh on 401 errors
- Offline mode detection (planned)

## External Dependencies

### Python Backend
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **SQLAlchemy**: ORM for database operations
- **Psycopg2**: PostgreSQL adapter
- **Pydantic**: Data validation and serialization
- **Python-Jose**: JWT token handling
- **Passlib + Bcrypt**: Password hashing
- **Twilio**: SMS messaging for SOS
- **Firebase-Admin**: Push notification service
- **Python-Multipart**: File upload support

### Flutter Mobile
- **http**: HTTP client for API requests
- **shared_preferences**: Local storage for tokens
- **provider**: State management (planned)
- **firebase_messaging**: FCM integration
- **flutter_local_notifications**: Local notification display

### Infrastructure
- **PostgreSQL**: Managed database via Replit
- **Twilio**: SMS service via Replit connector
- **Firebase**: Push notification and cloud messaging

### Development Tools
- **Streamlit**: MVP/prototype interface
- **Flutter SDK**: Mobile app development
- **UV**: Python package manager

## Workflows

### Configured Workflows
1. **Server** (Port 5000): `streamlit run app.py --server.port 5000`
2. **Backend API** (Port 8000): `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

### Deployment Configuration
- **Target**: VM (always-on for mobile API)
- **Command**: Backend API on port 5000 + Streamlit on port 8501
- **Strategy**: Backend serves mobile apps, Streamlit serves admin/prototype interface

## File Structure

```
/
├── app.py                          # Streamlit MVP entry point
├── pages/                          # Streamlit pages
├── backend/
│   ├── main.py                     # FastAPI application
│   ├── models.py                   # SQLAlchemy ORM models
│   ├── schemas.py                  # Pydantic schemas
│   ├── auth.py                     # JWT authentication
│   ├── database.py                 # Database connection
│   └── notifications.py            # Firebase push notifications
├── flutter_app/
│   ├── lib/
│   │   ├── main.dart              # Flutter entry point
│   │   ├── services/              # API and auth services
│   │   └── screens/               # UI screens
│   ├── android/                   # Android config
│   └── ios/                       # iOS config
├── API_DOCUMENTATION.md           # Complete API reference
├── SETUP_INSTRUCTIONS.md          # Setup and deployment guide
├── firebase-credentials.json      # Firebase Admin SDK credentials
└── pyproject.toml                 # Python dependencies
```

## Future Enhancement Points

**Mobile App**:
- Implement proper state management (Provider/Riverpod)
- Add offline mode with local SQLite cache
- Implement biometric authentication
- Add health device integrations (Apple Health, Google Fit)

**Backend**:
- Implement medication reminder scheduler
- Add appointment reminder notifications
- Create admin dashboard for user management
- Implement data export (PDF reports)
- Add analytics and usage tracking

**Infrastructure**:
- Set up CI/CD pipeline for mobile app builds
- Implement automated testing (unit, integration, E2E)
- Add monitoring and logging (Sentry, LogRocket)
- Implement database backups and disaster recovery

**Features**:
- Telemedicine integration
- Prescription photo OCR
- Health metric insights with AI
- Family account linking
- Doctor portal for appointment management
