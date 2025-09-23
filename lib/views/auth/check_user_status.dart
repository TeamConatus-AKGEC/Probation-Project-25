import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

class CheckUserStatus extends StatefulWidget {
  const CheckUserStatus({super.key});

  @override
  State<CheckUserStatus> createState() => _CheckUserStatusState();
}

class _CheckUserStatusState extends State<CheckUserStatus> {
  @override
  void initState() {
    //TODO: implement initState
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((c) {
      if (FirebaseAuth.instance.currentUser == null) {
        Navigator.pushReplacementNamed(context, "/login");
      } else {
        Navigator.pushReplacement(context, "/home" as Route<Object?>);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(child: CircularProgressIndicator(color: Colors.green)),
    );
  }
}
