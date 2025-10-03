import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService extends ChangeNotifier {
  // Use 10.0.2.2 for Android emulator, localhost for iOS simulator
  static String get baseUrl {
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    } else {
      return 'http://localhost:8000';
    }
  }
  
  String? _authToken;
  final int timeoutSeconds = 15;

  void setAuthToken(String token) {
    _authToken = token;
    notifyListeners();
  }

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (_authToken != null) 'Authorization': 'Bearer $_authToken',
      };

  // Helper method for error handling
  dynamic _handleResponse(http.Response response, {bool returnsList = false}) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return returnsList ? [] : {};
      return json.decode(response.body);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Resource not found');
    } else {
      final error = response.body.isNotEmpty ? json.decode(response.body) : {};
      throw Exception(error['detail'] ?? 'Request failed: ${response.statusCode}');
    }
  }

  // ==================== AUTH ====================
  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/login'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'username': username,
          'password': password,
        },
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Login failed: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> signup(
      String email, String username, String password, String fullName) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/signup'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'email': email,
          'username': username,
          'password': password,
          'full_name': fullName,
        }),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Signup failed: ${e.toString()}');
    }
  }

  // ==================== MEDICINES ====================
  Future<List<dynamic>> getMedicines() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/medicines'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response, returnsList: true);
    } catch (e) {
      throw Exception('Failed to load medicines: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> addMedicine(Map<String, dynamic> medicine) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/medicines'),
        headers: _headers,
        body: json.encode(medicine),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to add medicine: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> updateMedicine(int id, Map<String, dynamic> medicine) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/api/medicines/$id'),
        headers: _headers,
        body: json.encode(medicine),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to update medicine: ${e.toString()}');
    }
  }

  Future<void> deleteMedicine(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/api/medicines/$id'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to delete medicine: ${e.toString()}');
    }
  }

  // ==================== APPOINTMENTS ====================
  Future<List<dynamic>> getAppointments() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/appointments'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response, returnsList: true);
    } catch (e) {
      throw Exception('Failed to load appointments: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> addAppointment(Map<String, dynamic> appointment) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/appointments'),
        headers: _headers,
        body: json.encode(appointment),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to add appointment: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> updateAppointment(int id, Map<String, dynamic> appointment) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/api/appointments/$id'),
        headers: _headers,
        body: json.encode(appointment),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to update appointment: ${e.toString()}');
    }
  }

  Future<void> deleteAppointment(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/api/appointments/$id'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to delete appointment: ${e.toString()}');
    }
  }

  // ==================== HEALTH METRICS ====================
  Future<List<dynamic>> getHealthMetrics() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/health_metrics'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response, returnsList: true);
    } catch (e) {
      throw Exception('Failed to load health metrics: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> addHealthMetric(Map<String, dynamic> metric) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/health_metrics'),
        headers: _headers,
        body: json.encode(metric),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to add health metric: ${e.toString()}');
    }
  }

  // ==================== EMERGENCY CONTACTS ====================
  Future<List<dynamic>> getEmergencyContacts() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/emergency_contacts'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response, returnsList: true);
    } catch (e) {
      throw Exception('Failed to load emergency contacts: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> addEmergencyContact(Map<String, dynamic> contact) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/emergency_contacts'),
        headers: _headers,
        body: json.encode(contact),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to add emergency contact: ${e.toString()}');
    }
  }

  Future<void> deleteEmergencyContact(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/api/emergency_contacts/$id'),
        headers: _headers,
      ).timeout(Duration(seconds: timeoutSeconds));

      _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to delete emergency contact: ${e.toString()}');
    }
  }

  // ==================== SOS ====================
  Future<Map<String, dynamic>> sendSOS(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/sos'),
        headers: _headers,
        body: json.encode({'message': message}),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to send SOS: ${e.toString()}');
    }
  }

  Future<Map<String, dynamic>> sendSMS(String to, String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/send-sms'),
        headers: _headers,
        body: json.encode({'to': to, 'message': message}),
      ).timeout(Duration(seconds: timeoutSeconds));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Failed to send SMS: ${e.toString()}');
    }
  }

  // ==================== HEALTH CHECK ====================
  Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(Duration(seconds: 5));

      return _handleResponse(response);
    } catch (e) {
      throw Exception('Backend not reachable: ${e.toString()}');
    }
  }
}