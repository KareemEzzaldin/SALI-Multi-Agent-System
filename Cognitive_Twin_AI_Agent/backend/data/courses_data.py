"""
SALI Prototype — Sample Courses Data
Provides 2 full courses with structured concepts, course evidence grounding,
and pre-built misconception triggers for testing the AI Agents.
"""

STUDENT_PROFILE = {
    "student_id": "STD-2026-904",
    "name": "Kareem Ezzaldin",
    "email": "kareem.ezz.1972@gmail.com",
    "degree": "B.Sc. Artificial Intelligence & Software Systems",
    "semester": "Year 3, Fall 2026",
    "overall_cognitive_index": 0.72,
    "current_streak_days": 8,
    "memory_stability_days": 5.4
}

COURSES_DATA = [
    {
        "course_id": "CS-201",
        "course_title": "Python Systems & Memory Architecture",
        "code": "CS-201",
        "description": "Deep dive into memory layout, pointer mechanics, execution stacks, and runtime behavior.",
        "instructor": "Dr. Nadia Vance",
        "concepts": [
            {
                "concept_id": "c_ptr_mem",
                "concept_name": "Pointers & Object References",
                "mastery": 0.35,
                "stability": 2.4,
                "last_practiced": "2026-09-18",
                "course_evidence": (
                    "In Python, variables do not store raw values directly in place; instead, they hold object "
                    "references (pointers) pointing to heap-allocated objects. Assignment statements (a = b) bind "
                    "the name 'a' to the existing object reference of 'b' rather than cloning or deep-copying memory. "
                    "Mutating an object through one reference reflects in all aliases pointing to the identical memory address (id(a) == id(b))."
                ),
                "sample_question": {
                    "question_id": "q_ptr_01",
                    "question_text": "Given `list_a = [1, 2, 3]` and `list_b = list_a`, followed by `list_b.append(4)`, what is `list_a`?",
                    "correct_answer": "[1, 2, 3, 4] because list_a and list_b point to the same list in memory",
                    "misconception_presets": [
                        {
                            "title": "Pass-by-Value / Deep Copy Fallacy",
                            "answer": "[1, 2, 3] because assigning list_b creates an independent copy of list_a",
                            "expected_misconception": "Treating pointer/reference assignment as a separate value clone"
                        },
                        {
                            "title": "Immutable Rebinding Fallacy",
                            "answer": "Error: you cannot append to a list through another reference",
                            "expected_misconception": "Believing alias variables cannot mutate shared references"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_mut_args",
                "concept_name": "Mutable Default Arguments",
                "mastery": 0.58,
                "stability": 4.1,
                "last_practiced": "2026-09-19",
                "course_evidence": (
                    "Python evaluates default argument expressions once at the moment the function definition is executed, "
                    "NOT each time the function is called. When a mutable default argument like a list or dictionary "
                    "is modified inside the function body, that mutated object persists across subsequent calls."
                ),
                "sample_question": {
                    "question_id": "q_mut_01",
                    "question_text": "def add_item(val, items=[]):\n    items.append(val)\n    return items\nWhat does calling add_item(1) then add_item(2) return?",
                    "correct_answer": "[1, 2] because the default list is created once at definition time and shared across invocations",
                    "misconception_presets": [
                        {
                            "title": "Invocation-Time Evaluation Fallacy",
                            "answer": "[2] because items gets re-initialized as a new empty list [] on each call",
                            "expected_misconception": "Assuming default parameters are freshly instantiated on each invocation"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_rec_stack",
                "concept_name": "Recursion & Call Stack Frames",
                "mastery": 0.42,
                "stability": 2.8,
                "last_practiced": "2026-09-17",
                "course_evidence": (
                    "Every recursive call creates an independent stack frame on the call stack preserving local variables. "
                    "A recursive function MUST have an explicit base case condition to halt the recursion; otherwise, the call "
                    "stack grows unbounded until reaching sys.getrecursionlimit(), triggering a RecursionError."
                ),
                "sample_question": {
                    "question_id": "q_rec_01",
                    "question_text": "What causes a Python program with recursion to throw RecursionError: maximum recursion depth exceeded?",
                    "correct_answer": "Lack of a reached base case causing stack frames to accumulate without unwinding",
                    "misconception_presets": [
                        {
                            "title": "Implicit Termination Fallacy",
                            "answer": "The function automatically detects when to stop based on variable decrease",
                            "expected_misconception": "Believing runtime stops recursion automatically without explicit base cases"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_scope_lex",
                "concept_name": "Variable Scope & Closures",
                "mastery": 0.81,
                "stability": 9.5,
                "last_practiced": "2026-09-15",
                "course_evidence": (
                    "Python resolves variable names following the LEGB rule (Local, Enclosing, Global, Built-in). "
                    "Assigning to a variable inside a function makes it local unless explicitly declared with 'global' or 'nonlocal'."
                ),
                "sample_question": {
                    "question_id": "q_scp_01",
                    "question_text": "Inside a nested function, which keyword allows rebinding a variable defined in the enclosing non-global scope?",
                    "correct_answer": "nonlocal",
                    "misconception_presets": [
                        {
                            "title": "Global Confusion",
                            "answer": "global",
                            "expected_misconception": "Conflating global module-level scope with enclosing closure scope"
                        }
                    ]
                }
            }
        ]
    },
    {
        "course_id": "CS-301",
        "course_title": "Data Structures & Algorithmic Complexity",
        "code": "CS-301",
        "description": "Analysis of data structures, graph representations, heap management, and asymptotic efficiency.",
        "instructor": "Prof. Omar Farooq",
        "concepts": [
            {
                "concept_id": "c_dyn_arr",
                "concept_name": "Dynamic Arrays & Amortized Resizing",
                "mastery": 0.76,
                "stability": 8.0,
                "last_practiced": "2026-09-16",
                "course_evidence": (
                    "Dynamic arrays allocate continuous blocks of contiguous memory. When capacity is exceeded, they allocate "
                    "a new array of double (or 1.5x) the size and copy all elements over in O(N) time. However, across N appends, "
                    "the average cost per append remains amortized O(1)."
                ),
                "sample_question": {
                    "question_id": "q_arr_01",
                    "question_text": "What is the amortized time complexity of appending an element to a dynamic array (like Python list)?",
                    "correct_answer": "Amortized O(1)",
                    "misconception_presets": [
                        {
                            "title": "Worst-case conflation",
                            "answer": "Always O(N) because the array always resizes every single insert",
                            "expected_misconception": "Confusing occasional O(N) resizing cost with everyday O(1) append"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_hash_coll",
                "concept_name": "Hash Tables & Collision Resolution",
                "mastery": 0.49,
                "stability": 3.6,
                "last_practiced": "2026-09-18",
                "course_evidence": (
                    "A hash table maps keys to indices using a hash function. When two distinct keys compute the same index, "
                    "a collision occurs. Common strategies to resolve collisions include Separate Chaining (linked lists at each bucket) "
                    "and Open Addressing with probing (Linear Probing, Quadratic Probing)."
                ),
                "sample_question": {
                    "question_id": "q_hash_01",
                    "question_text": "In a hash table using separate chaining, what happens to lookup performance if all N keys hash to the same bucket?",
                    "correct_answer": "Degrades from average O(1) to worst-case O(N) linear scan",
                    "misconception_presets": [
                        {
                            "title": "Collision Overwrite Fallacy",
                            "answer": "The new key simply overwrites the old key and deletes it",
                            "expected_misconception": "Assuming hash tables overwrite colliding entries without resolution"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_bst_bal",
                "concept_name": "Binary Search Trees & Balancing",
                "mastery": 0.64,
                "stability": 6.2,
                "last_practiced": "2026-09-14",
                "course_evidence": (
                    "A Binary Search Tree maintains the invariant: left child < node < right child. In a balanced BST, "
                    "search, insert, and delete operate in O(log N). If inserted in sorted order without rebalancing, "
                    "the tree degenerates into a linked list with O(N) height."
                ),
                "sample_question": {
                    "question_id": "q_bst_01",
                    "question_text": "What is the worst-case height and search complexity of an un-balanced BST with N nodes?",
                    "correct_answer": "Height N and search time O(N)",
                    "misconception_presets": [
                        {
                            "title": "Guaranteed Logarithmic Fallacy",
                            "answer": "Search is always O(log N) no matter what order nodes are inserted",
                            "expected_misconception": "Believing standard BSTs automatically self-balance like AVL or Red-Black trees"
                        }
                    ]
                }
            }
        ]
    }
]
