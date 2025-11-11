// lib/home_screen.dart
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:animate_do/animate_do.dart';
import 'package:google_fonts/google_fonts.dart';
import 'profile_screen.dart'; // <-- ADD THIS IMPORT

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final CollectionReference _todosCollection =
  FirebaseFirestore.instance.collection('todos');
  final User? currentUser = FirebaseAuth.instance.currentUser; // <-- Get the full user object
  final TextEditingController _textController = TextEditingController();

  // ... (All your other functions _addTodo, _toggleTodoStatus, etc. remain unchanged)
  Future<void> _addTodo() async {
    final text = _textController.text;
    if (text.isEmpty || currentUser == null) {
      return;
    }
    try {
      await _todosCollection.add({
        'title': text,
        'isDone': false,
        'createdAt': Timestamp.now(),
        'userId': currentUser!.uid,
      });
      if (!mounted) return;
      _textController.clear();
      Navigator.of(context).pop();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Failed to add todo. Please check your connection."),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _toggleTodoStatus(DocumentSnapshot todo) async {
    await _todosCollection.doc(todo.id).update({
      'isDone': !todo['isDone'],
    });
  }

  Future<void> _deleteTodo(String todoId) async {
    await _todosCollection.doc(todoId).delete();
  }

  void _showAddTodoDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
          title: Text('Add a new todo', style: GoogleFonts.poppins()),
          content: TextField(
            controller: _textController,
            autofocus: true,
            decoration: const InputDecoration(labelText: 'Todo title'),
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                _textController.clear();
                Navigator.of(context).pop();
              },
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF6366F1),
                foregroundColor: Colors.white,
              ),
              onPressed: _addTodo,
              child: const Text('Add'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    // Get the first letter of the user's email for the avatar
    final String userEmail = currentUser?.email ?? 'U';
    final String avatarLetter = userEmail.isNotEmpty ? userEmail[0].toUpperCase() : 'U';

    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F7),
      appBar: AppBar(
        title: Text('My Todos', style: GoogleFonts.poppins(fontWeight: FontWeight.w600)),
        centerTitle: false, // <-- Changed to false to align title left
        backgroundColor: const Color(0xFF4A5568),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          // ======== START: MODIFIED SECTION ========
          // Profile Avatar Button
          GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ProfileScreen()),
              );
            },
            child: CircleAvatar(
              backgroundColor: const Color(0xFF6366F1),
              child: Text(
                avatarLetter,
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          const SizedBox(width: 10),

          // Logout Button
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              FirebaseAuth.instance.signOut();
            },
          ),
          const SizedBox(width: 10),
          // ======== END: MODIFIED SECTION ========
        ],
      ),
      body: StreamBuilder(
        // Use currentUser.uid in the stream query
        stream: _todosCollection
            .where('userId', isEqualTo: currentUser?.uid)
            .orderBy('createdAt', descending: true)
            .snapshots(),
        builder: (context, AsyncSnapshot<QuerySnapshot> streamSnapshot) {
          // ... The rest of your body StreamBuilder is completely unchanged
          if (streamSnapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(color: Color(0xFF6366F1)));
          }
          if (!streamSnapshot.hasData || streamSnapshot.data!.docs.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.check_circle_outline, size: 80, color: Colors.grey[300]),
                  const SizedBox(height: 16),
                  Text(
                    'All tasks completed!',
                    style: GoogleFonts.poppins(fontSize: 18, color: Colors.grey),
                  ),
                ],
              ),
            );
          }
          return ListView.builder(
            itemCount: streamSnapshot.data!.docs.length,
            itemBuilder: (context, index) {
              final DocumentSnapshot documentSnapshot =
              streamSnapshot.data!.docs[index];
              return FadeInUp(
                duration: const Duration(milliseconds: 300),
                child: Dismissible(
                  key: Key(documentSnapshot.id),
                  direction: DismissDirection.endToStart,
                  onDismissed: (direction) {
                    _deleteTodo(documentSnapshot.id);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Todo deleted')),
                    );
                  },
                  background: Container(
                    color: const Color(0xFFE57373),
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    alignment: Alignment.centerRight,
                    child: const Icon(Icons.delete, color: Colors.white),
                  ),
                  child: Card(
                    margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    elevation: 2,
                    shadowColor: Colors.black.withOpacity(0.1),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    child: CheckboxListTile(
                      activeColor: const Color(0xFF6366F1),
                      title: Text(
                        documentSnapshot['title'],
                        style: GoogleFonts.poppins(
                            decoration: documentSnapshot['isDone']
                                ? TextDecoration.lineThrough
                                : TextDecoration.none,
                            color: documentSnapshot['isDone']
                                ? Colors.grey[500]
                                : const Color(0xFF4A5568),
                            fontWeight: FontWeight.w500
                        ),
                      ),
                      value: documentSnapshot['isDone'],
                      onChanged: (bool? value) {
                        _toggleTodoStatus(documentSnapshot);
                      },
                    ),
                  ),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddTodoDialog,
        backgroundColor: const Color(0xFF6366F1),
        child: const Icon(Icons.add, color: Colors.white),
      ),
    );
  }
}