import 'package:ecommerce1/providers/user_provider.dart';
import 'package:ecommerce1/views/auth/bottomnav/navpages/defaul_page.dart';
import 'package:ecommerce1/views/auth/bottomnav/navpages/user_cart.dart';
import 'package:ecommerce1/views/splash/splash_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart' show ChangeNotifierProvider, MultiProvider;
import 'views/auth/bottomnav/homepage.dart';
// import 'views/auth/create_account_page.dart';
// import 'views/auth/loginpage.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => UserProvider()),
        
      ],
      child: MaterialApp(
        title: 'Byte_Basket',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        initialRoute: "/splash",
        routes: {
          "/splash": (context) => const SplashScreen(),
          // "/signup": (context) => const CreateAccountPage(),
          // "/login": (context) => const Loginpage(),
          "/home": (context) => const HomePage(),
          "/default": (context) => const DefaultPage(),
          "/cart": (context) => const CartPage(),
        },
      ),
    );
  }
}
