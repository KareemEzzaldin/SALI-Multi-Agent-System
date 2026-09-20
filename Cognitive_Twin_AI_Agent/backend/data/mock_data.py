"""
SALI — Mock Data
Three pre-built learner personas for demo purposes.
"""
from datetime import date, timedelta

TODAY = date.today().isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()
WEEK_AGO = (date.today() - timedelta(days=7)).isoformat()
TWO_WEEKS_AGO = (date.today() - timedelta(days=14)).isoformat()

# ─────────────────────────────────────────────
# COURSE EVIDENCE LIBRARY
# ─────────────────────────────────────────────

COURSE_EVIDENCE_LIBRARY = {
    "Python Functions": {
        "concept_name": "Python Functions",
        "source_text": (
            "A Python function is a reusable block of code defined with the `def` keyword. "
            "Functions encapsulate logic and accept parameters, which are local variables "
            "that receive values (arguments) when the function is called. "
            "The `return` statement sends a value back to the caller. "
            "Without an explicit `return`, a function implicitly returns `None`. "
            "Parameters vs Arguments: 'parameters' are the names listed in the function definition; "
            "'arguments' are the values passed during the call. "
            "Default parameter values allow optional arguments. "
            "Example: `def greet(name='World'): return f'Hello, {name}!'`"
        ),
    },
    "Recursion": {
        "concept_name": "Recursion",
        "source_text": (
            "Recursion is a technique where a function calls itself to solve a smaller sub-problem. "
            "Every recursive function must have a BASE CASE — a condition that stops the recursion "
            "to prevent infinite loops and stack overflow errors. "
            "The RECURSIVE CASE is the part where the function calls itself with a simpler input. "
            "Example (factorial): `def factorial(n): return 1 if n <= 1 else n * factorial(n-1)`. "
            "The call stack grows with each recursive call; deep recursion can hit Python's "
            "default recursion limit of 1000. "
            "Tail recursion is NOT optimized in CPython — use iteration for deep problems."
        ),
    },
    "List Comprehensions": {
        "concept_name": "List Comprehensions",
        "source_text": (
            "A list comprehension provides a concise way to create lists. "
            "Syntax: `[expression for item in iterable if condition]`. "
            "They are generally faster than equivalent for-loops because the iteration "
            "is performed at C speed internally. "
            "Example: `squares = [x**2 for x in range(10) if x % 2 == 0]`. "
            "Nested comprehensions are possible but reduce readability. "
            "For side-effects only (no list needed), prefer a regular for-loop."
        ),
    },
}

# ─────────────────────────────────────────────
# LEARNER PERSONAS
# ─────────────────────────────────────────────

LEARNER_PERSONAS = {
    "learner_001": {
        "learner_history": {
            "learner_id": "learner_001",
            "learner_name": "Alex (Struggling)",
            "attempts": [
                {
                    "attempt_number": 1,
                    "question_id": "q_func_001",
                    "question_text": "What does a Python function return if it has no return statement?",
                    "correct_answer": "None",
                    "learner_answer": "Nothing / an error",
                    "is_correct": False,
                    "timestamp": f"{TWO_WEEKS_AGO}T09:00:00Z",
                },
                {
                    "attempt_number": 2,
                    "question_id": "q_func_001",
                    "question_text": "What does a Python function return if it has no return statement?",
                    "correct_answer": "None",
                    "learner_answer": "0",
                    "is_correct": False,
                    "timestamp": f"{WEEK_AGO}T10:00:00Z",
                },
                {
                    "attempt_number": 3,
                    "question_id": "q_func_002",
                    "question_text": "What is the difference between a parameter and an argument?",
                    "correct_answer": "Parameters are in the definition; arguments are the values passed at call time.",
                    "learner_answer": "They are the same thing.",
                    "is_correct": False,
                    "timestamp": f"{YESTERDAY}T14:00:00Z",
                },
            ],
            "mastery_vector": [
                {"concept_name": "Python Functions", "mastery_score": 0.18, "last_practiced": YESTERDAY},
                {"concept_name": "Recursion", "mastery_score": 0.05, "last_practiced": TWO_WEEKS_AGO},
                {"concept_name": "List Comprehensions", "mastery_score": 0.10, "last_practiced": WEEK_AGO},
                {"concept_name": "Variables & Types", "mastery_score": 0.55, "last_practiced": TODAY},
                {"concept_name": "Control Flow", "mastery_score": 0.40, "last_practiced": YESTERDAY},
                {"concept_name": "Loops", "mastery_score": 0.35, "last_practiced": WEEK_AGO},
            ],
        },
        "current_interaction": {
            "question_id": "q_func_003",
            "question_text": "What keyword is used to define a function in Python?",
            "correct_answer": "def",
            "learner_answer": "function",
            "is_correct": False,
        },
        "course_evidence": COURSE_EVIDENCE_LIBRARY["Python Functions"],
    },

    "learner_002": {
        "learner_history": {
            "learner_id": "learner_002",
            "learner_name": "Sam (Progressing)",
            "attempts": [
                {
                    "attempt_number": 1,
                    "question_id": "q_rec_001",
                    "question_text": "What prevents a recursive function from running forever?",
                    "correct_answer": "A base case",
                    "learner_answer": "It just stops eventually",
                    "is_correct": False,
                    "timestamp": f"{WEEK_AGO}T09:00:00Z",
                },
                {
                    "attempt_number": 2,
                    "question_id": "q_rec_001",
                    "question_text": "What prevents a recursive function from running forever?",
                    "correct_answer": "A base case",
                    "learner_answer": "A base case stops the recursion",
                    "is_correct": True,
                    "timestamp": f"{YESTERDAY}T11:00:00Z",
                },
            ],
            "mastery_vector": [
                {"concept_name": "Python Functions", "mastery_score": 0.72, "last_practiced": TODAY},
                {"concept_name": "Recursion", "mastery_score": 0.45, "last_practiced": YESTERDAY},
                {"concept_name": "List Comprehensions", "mastery_score": 0.60, "last_practiced": WEEK_AGO},
                {"concept_name": "Variables & Types", "mastery_score": 0.85, "last_practiced": TODAY},
                {"concept_name": "Control Flow", "mastery_score": 0.78, "last_practiced": YESTERDAY},
                {"concept_name": "Loops", "mastery_score": 0.70, "last_practiced": WEEK_AGO},
            ],
        },
        "current_interaction": {
            "question_id": "q_rec_002",
            "question_text": "Write the base case for a recursive factorial function.",
            "correct_answer": "if n <= 1: return 1",
            "learner_answer": "if n == 0: return 1",
            "is_correct": True,
        },
        "course_evidence": COURSE_EVIDENCE_LIBRARY["Recursion"],
    },

    "learner_003": {
        "learner_history": {
            "learner_id": "learner_003",
            "learner_name": "Jordan (Advanced)",
            "attempts": [
                {
                    "attempt_number": 1,
                    "question_id": "q_lc_001",
                    "question_text": "What is the syntax structure of a list comprehension?",
                    "correct_answer": "[expression for item in iterable if condition]",
                    "learner_answer": "[expression for item in iterable if condition]",
                    "is_correct": True,
                    "timestamp": f"{WEEK_AGO}T08:00:00Z",
                },
                {
                    "attempt_number": 2,
                    "question_id": "q_lc_002",
                    "question_text": "Write a list comprehension for even squares up to 10.",
                    "correct_answer": "[x**2 for x in range(10) if x % 2 == 0]",
                    "learner_answer": "[x**2 for x in range(10) if x % 2 == 0]",
                    "is_correct": True,
                    "timestamp": f"{YESTERDAY}T10:00:00Z",
                },
            ],
            "mastery_vector": [
                {"concept_name": "Python Functions", "mastery_score": 0.92, "last_practiced": TODAY},
                {"concept_name": "Recursion", "mastery_score": 0.88, "last_practiced": YESTERDAY},
                {"concept_name": "List Comprehensions", "mastery_score": 0.78, "last_practiced": YESTERDAY},
                {"concept_name": "Variables & Types", "mastery_score": 0.95, "last_practiced": TODAY},
                {"concept_name": "Control Flow", "mastery_score": 0.91, "last_practiced": TODAY},
                {"concept_name": "Loops", "mastery_score": 0.89, "last_practiced": YESTERDAY},
            ],
        },
        "current_interaction": {
            "question_id": "q_lc_003",
            "question_text": "When should you prefer a regular for-loop over a list comprehension?",
            "correct_answer": "When the goal is side effects only and no list is needed.",
            "learner_answer": "When you only need side effects and don't need to build a list.",
            "is_correct": True,
        },
        "course_evidence": COURSE_EVIDENCE_LIBRARY["List Comprehensions"],
    },
}
