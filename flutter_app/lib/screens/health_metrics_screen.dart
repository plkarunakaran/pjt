import 'package:flutter/material.dart';

class HealthMetricsScreen extends StatelessWidget {
  const HealthMetricsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: const Center(
        child: Text('Health Metrics Screen - Connected to Backend API'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Add health metric dialog
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
