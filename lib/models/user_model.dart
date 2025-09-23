class UserModel {
  String name;
  String email;
  String address;
  String phone;

  UserModel({
    required this.name,
    required this.address,
    required this.email,
    required this.phone,
  });

  factory UserModel.fromJson(Map<String, dynamic> jsonData) {
    return UserModel(
      name: jsonData["name"] ?? "",
      address: jsonData["address"] ?? "",
      email: jsonData["email"] ?? "",
      phone: jsonData["phoneS"] ?? "",
    );
  }
}
