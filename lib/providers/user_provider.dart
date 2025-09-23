import 'package:flutter/material.dart';

class UserProvider extends ChangeNotifier {
  String nameOfUser = "";
  String emailOfUser = "";
  String addressOfUser = "";
  String phonenumberOfUser = "";

  UserProvider() {
    getUserData(); 
  }

  
  void getUserData() {
    
    nameOfUser = "Guest User";
    emailOfUser = "guest@example.com";
    addressOfUser = "123 Flutter Street";
    phonenumberOfUser = "9999999999";

    notifyListeners();
  }

  
  void declineProvider() {
    nameOfUser = "";
    emailOfUser = "";
    addressOfUser = "";
    phonenumberOfUser = "";

    notifyListeners();
  }

  @override
  void dispose() {
    declineProvider();
    super.dispose();
  }
}
