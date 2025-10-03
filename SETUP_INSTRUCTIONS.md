# MedPal Setup Instructions

## Overview
MedPal is a comprehensive mobile health management application with:
- **Streamlit MVP**: Rapid prototyping interface on port 5000
- **FastAPI Backend**: Production API on port 8000
- **Flutter Mobile App**: Native iOS/Android application
- **PostgreSQL Database**: Secure data persistence
- **Twilio Integration**: Emergency SOS via SMS
- **Firebase**: Push notifications for medication reminders

## Architecture

```
┌─────────────────┐
│  Streamlit MVP  │ (Port 5000)
│  (Prototype)    │
└─────────────────┘

┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Flutter App    │────▶│  FastAPI     │────▶│  PostgreSQL  │
│  (Production)   │     │  Backend     │     │  Database    │
└─────────────────┘     └──────────────┘     └──────────────┘
                               │
                               ├─────▶ Twilio (SOS)
                               │
                               └─────▶ Firebase (Notifications)
```

## Environment Setup

### Required Environment Variables
The following secrets are automatically managed by Replit:
- `DATABASE_URL`: PostgreSQL connection string
- Twilio credentials (via Replit integration)
- Firebase credentials (stored in `firebase-credentials.json`)

### Python Dependencies
All dependencies are managed via `pyproject.toml`:
- FastAPI + Uvicorn
- SQLAlchemy + Psycopg2
- Streamlit
- Twilio SDK
- Firebase Admin SDK
- Pydantic, JWT, Bcrypt, etc.

## Running the Application

### 1. Streamlit MVP (Port 5000)
```bash
streamlit run app.py --server.port 5000
```

### 2. FastAPI Backend (Port 8000)
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Both workflows are pre-configured and will auto-start.

## Database Setup

### Initial Migration
The database tables are automatically created on first run via SQLAlchemy:
- `users`
- `medicines`
- `appointments`
- `health_metrics`
- `emergency_contacts`

### Schema Changes
If you modify `backend/models.py`, restart the backend workflow to apply changes.

## API Endpoints

See `API_DOCUMENTATION.md` for complete API reference.

Key endpoints:
- `POST /api/signup` - User registration
- `POST /api/login` - User authentication
- `GET /api/medicines` - Get medicines
- `POST /api/sos` - Send emergency SOS

## Flutter Mobile App

### Prerequisites
1. Install Flutter SDK: https://flutter.dev/docs/get-started/install
2. Install Android Studio or Xcode for device emulation

### Setup
```bash
cd flutter_app
flutter pub get
```

### Configuration
Update `lib/services/api_service.dart` with your backend URL:
```dart
static const String baseUrl = 'https://your-backend-url.repl.co';
```

### Run
```bash
flutter run
```

### Build for Production
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## Firebase Push Notifications

### Setup Firebase
1. Create a Firebase project: https://console.firebase.google.com
2. Add Android/iOS apps to the project
3. Download `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
4. Place them in respective Flutter directories
5. Upload Firebase Admin SDK credentials as `firebase-credentials.json`

### Notification Scheduler
The backend includes a notification scheduler in `backend/notifications.py` that:
- Checks for upcoming medicines/appointments
- Sends FCM push notifications
- Runs on a configurable schedule

## Twilio Emergency SOS

### Configuration
Twilio is pre-configured via Replit integration. The SOS feature:
- Sends SMS to all emergency contacts
- Includes user location (if provided)
- Logs all emergency requests

### Testing
```bash
curl -X POST http://localhost:8000/api/sos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test emergency message"}'
```

## Deployment

### Backend Deployment (Replit)
1. Click the "Publish" button in Replit
2. Configure autoscale deployment for the FastAPI backend
3. Note your deployment URL

### Mobile App Deployment

#### Google Play Store
1. Build release APK: `flutter build apk --release`
2. Create a Google Play Developer account
3. Upload APK via Google Play Console
4. Complete store listing and submit for review

#### Apple App Store
1. Build release IPA: `flutter build ipa --release`
2. Enroll in Apple Developer Program
3. Upload via App Store Connect
4. Complete app metadata and submit for review

## Development Workflow

1. **Prototype in Streamlit**: Quickly test UI/UX ideas
2. **Implement in Backend**: Add API endpoints in FastAPI
3. **Build Flutter UI**: Create mobile screens consuming the API
4. **Test**: Use Streamlit MVP for validation
5. **Deploy**: Publish backend + mobile apps

## Security Considerations

- All passwords are hashed with bcrypt
- JWT tokens for authentication
- Environment variables for secrets
- HTTPS for production deployment
- Input validation on all endpoints

## Troubleshooting

### Backend won't start
- Check `DATABASE_URL` is set
- Verify all dependencies are installed
- Review logs in workflow console

### Database connection errors
- Ensure PostgreSQL is running
- Verify credentials in environment

### Flutter build errors
- Run `flutter clean && flutter pub get`
- Check Firebase configuration files
- Verify API URL is correct

## Support

For issues or questions:
- Check API documentation: `API_DOCUMENTATION.md`
- Review code comments in source files
- Test endpoints via Streamlit MVP
