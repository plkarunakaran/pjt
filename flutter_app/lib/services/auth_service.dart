import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService extends ChangeNotifier {
  String? _token;
  String? _username;
  bool _isAuthenticated = false;
  bool _isLoading = true;

  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;
  String? get token => _token;
  String? get username => _username;

  AuthService() {
    checkAuthStatus();
  }

  Future<void> checkAuthStatus() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      final prefs = await SharedPreferences.getInstance();
      _token = prefs.getString('auth_token');
      _username = prefs.getString('username');
      _isAuthenticated = _token != null;
    } catch (e) {
      debugPrint('Error checking auth status: $e');
      _isAuthenticated = false;
    }
    
    _isLoading = false;
    notifyListeners();
  }

  Future<void> login(String token, String username) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', token);
      await prefs.setString('username', username);
      
      _token = token;
      _username = username;
      _isAuthenticated = true;
      
      notifyListeners();
    } catch (e) {
      debugPrint('Error saving auth data: $e');
      throw Exception('Failed to save login data');
    }
  }

  Future<void> logout() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('auth_token');
      await prefs.remove('username');
      
      _token = null;
      _username = null;
      _isAuthenticated = false;
      
      notifyListeners();
    } catch (e) {
      debugPrint('Error during logout: $e');
    }
  }

  Future<void> updateProfile(String username) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('username', username);
      _username = username;
      notifyListeners();
    } catch (e) {
      debugPrint('Error updating profile: $e');
    }
  }
}