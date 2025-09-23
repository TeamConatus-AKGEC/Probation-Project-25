
import 'package:flutter/material.dart';

class Loginpage extends StatefulWidget {
  const Loginpage({super.key});

  @override
  State<Loginpage> createState() => _LoginpageState();
}

class _LoginpageState extends State<Loginpage> {
  final formGlobalKey = GlobalKey<FormState>();
  TextEditingController emailTextEditingController = TextEditingController();
  TextEditingController passwordTextEditingController = TextEditingController();
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              Image.asset("assets/images/loginicon.png"),
              const SizedBox(height: 20),
              Text(
                "Welcome Back",
                 style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 6),
              Text(
                "Login to continue",
                style: TextStyle(fontSize: 16, color: Colors.grey.shade600),
              ),
              Form(
                key: formGlobalKey,
                child: Column(
                  children: [
                    const SizedBox(height: 10),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      child: TextFormField(
                        validator: (value) =>
                            value!.isEmpty ? "Email cannot be empty." : null,
                        controller: emailTextEditingController,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          label: Text("Email"),
                        ),
                      ),
                    ),
                    const SizedBox(height: 10),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      child: TextFormField(
                        validator: (value) => value!.length < 8
                            ? "Password should have at least 8 character."
                            : null,
                        controller: passwordTextEditingController,
                        obscureText: true,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          label: Text("Password"),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * .9,
                      height: 50,
                      child: ElevatedButton(
                        onPressed: () {
                          
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green,
                          foregroundColor: Colors.white,
                        ),
                        child: const Text(
                          "login",
                          style: TextStyle(fontSize: 16),
                        ),
                      ),
                    ),
                    const SizedBox(height: 15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text("Don't have an account"),
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, "/signup");
                          },
                          child: const Text("sign ups"),
                        ),
                      ],
                    ),
                    const SizedBox(height: 30),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
