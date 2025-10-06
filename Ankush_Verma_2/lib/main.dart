// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart'; // 1. Import the package
import 'firebase_options.dart';
import 'auth_screen.dart';
import 'home_screen.dart';

void main() async {
  // We need to preserve the splash screen until we're done with init
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding); // 2. Preserve the splash screen

  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Firebase Auth',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: StreamBuilder<User?>(
        stream: FirebaseAuth.instance.authStateChanges(),
        builder: (context, snapshot) {
          // The stream is still waiting for the first event
          if (snapshot.connectionState == ConnectionState.waiting) {
            // While waiting, the native splash screen is still visible.
            // We return an empty container to not show anything over it.
            return const SizedBox.shrink();
          }

          // Once we have data, we can remove the splash screen.
          FlutterNativeSplash.remove(); // 3. Remove splash screen

          if (snapshot.hasData) {
            // If user is logged in, show HomeScreen
            return const HomeScreen();
          } else {
            // If user is not logged in, show AuthScreen
            return const AuthScreen();
          }
        },
      ),
    );
  }
}