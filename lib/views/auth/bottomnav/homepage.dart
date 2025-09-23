import 'package:flutter/material.dart';
// ignore: unused_import
import 'package:provider/provider.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int chosenIndex = 0;

  
  late List<Widget> navpages;

  @override
  void initState() {
    super.initState();
    navpages = const [
    Center(child: Text("Home Page Loaded")),
    Center(child: Text("Orders Page Loaded")),
    Center(child: Text("Cart Page Loaded")),
    Center(child: Text("Profile Page Loaded")),       
    ];
  }

  @override
  Widget build(BuildContext context) {
    
    return Scaffold(
      body: navpages[chosenIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: chosenIndex,
        onTap: (index) {
          setState(() {
            chosenIndex = index;
          });
        },
        selectedItemColor: Colors.green,
        unselectedItemColor: Colors.grey,
        showSelectedLabels: true,
        showUnselectedLabels: true,
        items: [
          const BottomNavigationBarItem(
            icon: Icon(Icons.home_outlined),
            label: "Home",
          ),
          const BottomNavigationBarItem(
            icon: Icon(Icons.local_shipping_outlined),
            label: "Orders",
          ),

         
          BottomNavigationBarItem(
            icon: Stack(
              children: [
                const Icon(Icons.shopping_cart_outlined),
                
                  Positioned(
                    right: 0,
                    child: Container(
                      padding: const EdgeInsets.all(2),
                      decoration: const BoxDecoration(
                        color: Colors.red,
                        shape: BoxShape.circle,
                      ),
                      constraints: const BoxConstraints(
                        minWidth: 16,
                        minHeight: 16,
                      ),
                      
                    ),
                  ),
              ],
            ),
            label: "Cart",
          ),

          const BottomNavigationBarItem(
            icon: Icon(Icons.manage_accounts_outlined),
            label: "Profile",
          ),
        ],
      ),
    );
  }
}
