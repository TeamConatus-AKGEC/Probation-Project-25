import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:html_unescape/html_unescape.dart'; // <-- 1. ADD THIS IMPORT

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  // --- 2. REFACTORED STATE MANAGEMENT ---
  // Use a single string for the selected category instead of multiple booleans.
  String _selectedCategory = "music";

  // State for quiz data
  String question = "";
  String answer = "";
  List<String> options = [];
  bool answerNow = false;

  // Helper for decoding HTML entities from the API response
  final HtmlUnescape unescape = HtmlUnescape();

  @override
  void initState() {
    super.initState();
    // Load initial quiz data for the default category
    loadQuizData(_selectedCategory);
  }

  // No longer need _getSelectedCategory(), we just use _selectedCategory directly.

  void loadQuizData(String category) async {
    // Clear previous options and reset state
    setState(() {
      options.clear();
      question = "";
      answer = "";
      answerNow = false;
    });
    await fetchQuiz(category);
  }

  Future<void> fetchQuiz(String category) async {
    // --- 3. CORRECTED CATEGORY DATA ---
    // Replaced non-existent "food" with a valid "history" category.
    final Map<String, int> categoryIds = {
      "music": 12,
      "geography": 22,
      "history": 23, // "Food" (25) is not a valid category, replaced with "History"
      "science & nature": 17,
      "entertainment": 11,
    };

    final categoryId = categoryIds[category.toLowerCase()] ?? 12; // Default to music
    final url =
        'https://opentdb.com/api.php?amount=1&category=$categoryId&type=multiple';

    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        if (data['results'] != null && data['results'].isNotEmpty) {
          var quizData = data['results'][0];

          // --- 4. CRITICAL FIX: USE HTML UNESCAPE ---
          // Uri.decodeFull is wrong. Use unescape.convert() to fix characters like &quot;
          setState(() {
            question = unescape.convert(quizData['question']);
            answer = unescape.convert(quizData['correct_answer']);
            options = List<String>.from(quizData['incorrect_answers'])
                .map((opt) => unescape.convert(opt))
                .toList();
            options.add(answer);
            options.shuffle(); // Shuffle directly here
          });
        }
      } else {
        // Handle API error
        setState(() {
          question = "Failed to load question. Please check your connection.";
        });
      }
    } catch (e) {
      // Handle network or other errors
      print(e);
      setState(() {
        question = "An error occurred. Please try again later.";
      });
    }
  }

  void updateCategorySelection(String category) {
    // Only reload data if the category has changed
    if (_selectedCategory != category) {
      setState(() {
        _selectedCategory = category;
      });
      loadQuizData(category);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        height: MediaQuery.of(context).size.height,
        width: MediaQuery.of(context).size.width,
        child: Stack(
          children: [
            Image.asset(
              "assets/images/background.jpg",
              height: MediaQuery.of(context).size.height,
              width: MediaQuery.of(context).size.width,
              fit: BoxFit.cover,
            ),
            SafeArea( // Use SafeArea to avoid UI overlapping with status bar
              child: Column(
                children: [
                  const SizedBox(height: 20.0),
                  buildCategoryRow(),
                  const SizedBox(height: 30.0),
                  (options.isEmpty || question.isEmpty)
                      ? const Expanded(
                    child: Center(
                        child: CircularProgressIndicator(
                          color: Colors.white,
                        )),
                  )
                      : buildQuizContainer(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildCategoryRow() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20.0),
      height: 60,
      child: ListView(
        scrollDirection: Axis.horizontal,
        shrinkWrap: true,
        children: [
          // Simplified category chip creation
          buildCategoryChip("Music", "music"),
          buildCategoryChip("Geography", "geography"),
          buildCategoryChip("History", "history"),
          buildCategoryChip("Science", "science & nature"),
          buildCategoryChip("Entertainment", "entertainment"),
        ],
      ),
    );
  }

  Widget buildCategoryChip(String title, String categoryKey) {
    final bool isSelected = _selectedCategory == categoryKey; // Check against the single state variable
    return GestureDetector(
      onTap: () => updateCategorySelection(categoryKey),
      child: Material(
        elevation: 5.0,
        borderRadius: BorderRadius.circular(30),
        child: Container(
          margin: const EdgeInsets.only(right: 10.0),
          padding:
          const EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
          decoration: BoxDecoration(
            color: isSelected ? Colors.orange : Colors.white,
            borderRadius: BorderRadius.circular(30),
          ),
          child: Center(
            child: Text(
              title,
              style: TextStyle(
                color: isSelected ? Colors.white : Colors.black,
                fontSize: 18.0,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget buildQuizContainer() {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
        margin: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 20.0),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          children: [
            Text(
              question,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 22.0,
                color: Colors.black,
                fontWeight: FontWeight.bold,
              ),
            ),
            const Spacer(),
            ...options.map((option) => buildAnswerOption(option)).toList(),
            const Spacer(),
            // --- 5. IMPROVED UX: CONDITIONAL NEXT/SKIP BUTTON ---
            buildNextOrSkipButton(),
          ],
        ),
      ),
    );
  }

  Widget buildAnswerOption(String option) {
    Color borderColor = Colors.black45;
    Color? textColor; // Use default text color unless answered

    if (answerNow) {
      if (option == answer) {
        borderColor = Colors.green;
        textColor = Colors.green;
      } else {
        borderColor = Colors.red;
        textColor = Colors.red;
      }
    }

    return GestureDetector(
      onTap: () {
        if (!answerNow) {
          setState(() {
            answerNow = true;
          });
        }
      },
      child: Container(
        width: double.infinity,
        margin: const EdgeInsets.only(bottom: 20.0),
        padding: const EdgeInsets.all(15.0),
        decoration: BoxDecoration(
          border: Border.all(color: borderColor, width: 2.0),
          borderRadius: BorderRadius.circular(30),
        ),
        child: Center(
          child: Text(
            option,
            textAlign: TextAlign.center, // Better for long options
            style: TextStyle(
              color: textColor ?? Colors.black,
              fontSize: 18.0,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
      ),
    );
  }

  Widget buildNextOrSkipButton() {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.deepPurple,
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 10),
      ),
      onPressed: () {
        // Just load the next question regardless of whether we skip or advance
        loadQuizData(_selectedCategory);
      },
      child: Text(
        answerNow ? "Next" : "Skip", // Shows "Skip" before answering, "Next" after
        style: const TextStyle(
          fontSize: 18.0,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }
}