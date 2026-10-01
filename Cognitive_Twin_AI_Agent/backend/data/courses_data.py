"""
SALI — Primary 5 Courses Data (Egyptian Curriculum)
Richly structured for Primary 5 (الصف الخامس الابتدائي):
- Connect 5 (English)
- Mathematics (الرياضيات)
Includes multiple progressive questions per concept, rich explanation guides, options (MCQ), and pedagogical feedback.
"""

STUDENT_PROFILE = {
    "student_id": "STD-PRI5-104",
    "name": "كريم عز الدين (Kareem)",
    "email": "kareem.grade5@sali-learning.eg",
    "degree": "Primary 5 (Grade 5) — الصف الخامس الابتدائي",
    "grade_name": "الصف الخامس الابتدائي",
    "semester": "الفصل الدراسي الأول 2026/2027",
    "overall_cognitive_index": 0.68,
    "current_streak_days": 6,
    "memory_stability_days": 3.8
}

COURSES_DATA = [
    {
        "course_id": "ENG-501",
        "course_title": "English — Connect 5",
        "code": "ENG-501",
        "lang": "en",
        "description": "منهج اللغة الإنجليزية Connect 5 للصف الخامس الابتدائي (Grammar, Vocabulary & Ecosystems).",
        "instructor": "Teacher / مستر أحمد فاروق",
        "concepts": [
            {
                "concept_id": "c_past_simple",
                "concept_name": "Past Simple & Irregular Verbs",
                "arabic_title": "الماضي البسيط والأفعال غير المنتظمة",
                "mastery": 0.40,
                "stability": 2.2,
                "last_practiced": "2026-09-28",
                "course_evidence": (
                    "In Connect 5 Unit 1, regular past verbs take -ed (visited, played, traveled). "
                    "Irregular verbs change their form completely (go -> went, see -> saw, buy -> bought). "
                    "Negative sentences use 'didn't + infinitive' (He didn't go)."
                ),
                "explanation_guide": (
                    "أكيد يا بطل! 🌟 تعال نبسط قاعدة **الماضي البسيط (Past Simple)** بكل سهولة:\n\n"
                    "بنستخدم الماضي البسيط لما نتكلم عن أحداث بدأت وانتهت في الماضي (كلمات دالة: Yesterday, Last week, In the past, ago).\n\n"
                    "**1. الأفعال المنتظمة (Regular Verbs):**\n"
                    "أفعال بنضيف لآخرها `-ed` مثل:\n"
                    "- `visit ➔ visited` (زار)\n"
                    "- `travel ➔ traveled` (سافر)\n"
                    "- `play ➔ played` (لعب)\n\n"
                    "**2. الأفعال غير المنتظمة (Irregular Verbs):**\n"
                    "شكلها بيتغير تماماً وبنحفظها، ومش بنحط لها `-ed` أبداً:\n"
                    "- `go ➔ went` (ذهب)\n"
                    "- `buy ➔ bought` (اشترى)\n"
                    "- `make ➔ made` (صنع)\n\n"
                    "**3. النفي (Negative):**\n"
                    "بنستخدم `didn't` ويجي بعدها الفعل في المصدر (بدون أي إضافات):\n"
                    "- نقول: `He didn't go` (مش didn't went ❌)."
                ),
                "questions": [
                    {
                        "question_id": "q_past_1",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Yesterday, my family and I ______ to Alexandria and we ______ the Qaitbay Citadel.",
                        "hint": "Choose the past form: (go/travel) and (visit).",
                        "options": [
                            {"key": "A", "text": "went / visited", "is_correct": True},
                            {"key": "B", "text": "traveled / visited", "is_correct": True},
                            {"key": "C", "text": "goed / visited", "is_correct": False, "misconception": "Over-regularization: adding -ed to irregular 'go'"},
                            {"key": "D", "text": "go / visit", "is_correct": False, "misconception": "Using present base tense instead of past simple"}
                        ],
                        "accepted_text_answers": [
                            "went / visited", "went and visited", "went visited", "went, visited",
                            "traveled / visited", "traveled and visited", "traveled visited", "travelled / visited",
                            "travled / visited", "travled 2- visited", "1- travled 2- visited", "1- traveled 2- visited",
                            "1- went 2- visited", "went", "visited", "traveled", "A", "B"
                        ],
                        "pedagogical_success_reply": "أحسنت يا بطل! 🌟 إجابتك صحيحة وممتازة! استخدمت صيغة الماضي البسيط (went / traveled / visited) بشكل سليم جداً.",
                        "pedagogical_remediation_reply": "خد بالك يا بطل! 💡 في الماضي البسيط: الفعل go غير منتظم وماضيه went (مش بنحط له ed)، بينما visit و travel أفعال منتظمة بنضيف لها ed."
                    },
                    {
                        "question_id": "q_past_2",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Last Friday, Salma ______ a delicious chocolate cake, but she ______ any cookies.",
                        "hint": "Past of 'make' and negative past of 'make':",
                        "options": [
                            {"key": "A", "text": "made / didn't make", "is_correct": True},
                            {"key": "B", "text": "maked / didn't made", "is_correct": False, "misconception": "Adding -ed to irregular 'make'"},
                            {"key": "C", "text": "made / didn't made", "is_correct": False, "misconception": "Using past form after didn't"},
                            {"key": "D", "text": "make / doesn't make", "is_correct": False, "misconception": "Using present tense with 'last Friday'"}
                        ],
                        "accepted_text_answers": [
                            "made / didn't make", "made didn't make", "made", "didn't make", "A"
                        ],
                        "pedagogical_success_reply": "رائع جداً يا عبقري! 👏 الفعل make ماضيه made، وبعد didn't رجعنا الفعل لمصدره make بدون أي إضافات.",
                        "pedagogical_remediation_reply": "فكر فيها تاني يا بطل! 💡 الفعل make فعل غير منتظم ماضيه made، وبعد didn't دايماً بيجي الفعل في المصدر (didn't make)."
                    },
                    {
                        "question_id": "q_past_3",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Where ______ you ______ on your last summer holiday?",
                        "hint": "Past question format: did + subject + base verb",
                        "options": [
                            {"key": "A", "text": "did / go", "is_correct": True},
                            {"key": "B", "text": "did / went", "is_correct": False, "misconception": "Double past in questions"},
                            {"key": "C", "text": "do / went", "is_correct": False, "misconception": "Mixing present helper with past verb"},
                            {"key": "D", "text": "were / go", "is_correct": False, "misconception": "Using were with base verb"}
                        ],
                        "accepted_text_answers": [
                            "did / go", "did go", "did", "go", "A"
                        ],
                        "pedagogical_success_reply": "إجابة نموذجية! 🎯 في السؤال في الماضي بنستخدم did كفعل مساعد وبيجي معاها الفعل في المصدر go.",
                        "pedagogical_remediation_reply": "خد بالك يا شاطر! 💡 طالما استخدمنا did في السؤال، الفعل الأساسي بيرجع للمصدر go (مش went)."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "Over-regularization ('goed')",
                        "answer": "goed / visited",
                        "expected_misconception": "Adding -ed to irregular verb 'go' instead of using 'went'"
                    },
                    {
                        "title": "Double Past ('didn't went')",
                        "answer": "didn't went to Alexandria",
                        "expected_misconception": "Using past verb form after 'didn't' instead of base verb"
                    }
                ]
            },
            {
                "concept_id": "c_nouns_quantifiers",
                "concept_name": "Countable & Uncountable (Some / Any)",
                "arabic_title": "الأسماء المعدودة وغير المعدودة مع Some و Any",
                "mastery": 0.55,
                "stability": 3.4,
                "last_practiced": "2026-09-29",
                "course_evidence": (
                    "Countable nouns can be counted and have plural forms (apples). Uncountable nouns have no plural (water, milk). "
                    "Use 'many' with countable and 'much' with uncountable. "
                    "Use 'some' in positive sentences and offers, and 'any' in negative sentences and questions."
                ),
                "explanation_guide": (
                    "من عيوني يا بطل! 🍎🥛 تعال نفرق بين الأسماء المعدودة وغير المعدودة:\n\n"
                    "**1. الأسماء المعدودة (Countable Nouns):**\n"
                    "حاجات نقدر نعدها بالواحدة ولها مفرد وجمع:\n"
                    "- `an apple ➔ apples` 🍏\n"
                    "- `a carrot ➔ carrots` 🥕\n"
                    "- بنستخدم معاها `many` (كثير للعدد).\n\n"
                    "**2. الأسماء غير المعدودة (Uncountable Nouns):**\n"
                    "كميات وسوائل لا تُعد بالواحدة وليس لها جمع:\n"
                    "- `water` (ماء), `milk` (حليب), `rice` (أرز).\n"
                    "- بنستخدم معاها `much` (كثير للكمية)، ومينفعش نحط لها s في الآخر أبداً.\n\n"
                    "**3. استخدام Some و Any:**\n"
                    "- **Some (بعض):** في الجمل الإيجابية المثبتة، وعروض الضيافة والطلب (`Would you like some tea?`).\n"
                    "- **Any (أي):** في الجمل المنفية (`We don't have any...`) والأسئلة العادية (`Do you have any...?`)."
                ),
                "questions": [
                    {
                        "question_id": "q_nouns_1",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "We don't have ______ milk in the fridge, but we have ______ fresh apples.",
                        "hint": "Choose the correct pair of quantifiers:",
                        "options": [
                            {"key": "A", "text": "any / some", "is_correct": True},
                            {"key": "B", "text": "some / any", "is_correct": False, "misconception": "Using 'some' in negative statements"},
                            {"key": "C", "text": "many / much", "is_correct": False, "misconception": "Confusing many with uncountable milk"},
                            {"key": "D", "text": "a / any", "is_correct": False, "misconception": "Using 'a' with uncountable milk"}
                        ],
                        "accepted_text_answers": [
                            "any / some", "any some", "any, some", "any and some", "A"
                        ],
                        "pedagogical_success_reply": "رائع جداً! 👏 اخترت 'any' عشان الجملة منفية مع الحليب، و 'some' في الجملة المثبتة مع التفاح.",
                        "pedagogical_remediation_reply": "ركز يا بطل! 💡 في الجمل المنفية (don't have) بنستخدم 'any'، أما في الجمل المثبتة بنستخدم 'some'."
                    },
                    {
                        "question_id": "q_nouns_2",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Would you like ______ orange juice? — Yes, please!",
                        "hint": "This is a polite offer (عرض ضيافة مهذب):",
                        "options": [
                            {"key": "A", "text": "some (عرض ضيافة مهذب)", "is_correct": True},
                            {"key": "B", "text": "any", "is_correct": False, "misconception": "Using any in polite offers"},
                            {"key": "C", "text": "many", "is_correct": False, "misconception": "Using many with uncountable juice"},
                            {"key": "D", "text": "an", "is_correct": False, "misconception": "Using an with uncountable juice"}
                        ],
                        "accepted_text_answers": [
                            "some", "some (عرض ضيافة مهذب)", "A"
                        ],
                        "pedagogical_success_reply": "ممتاز! 🍊 في عروض الضيافة المهذبة (Would you like...) بنستخدم 'some' حتى لو كانت صيغة سؤال.",
                        "pedagogical_remediation_reply": "خد بالك يا شاطر! 💡 في عروض الكرم والضيافة المهذبة (Would you like...) بنستخدم 'some' مش 'any'."
                    },
                    {
                        "question_id": "q_nouns_3",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "How ______ bottles of water do we need, and how ______ water is in the glass?",
                        "hint": "Bottles are countable, water is uncountable:",
                        "options": [
                            {"key": "A", "text": "many / much", "is_correct": True},
                            {"key": "B", "text": "much / many", "is_correct": False, "misconception": "Reversing many and much"},
                            {"key": "C", "text": "some / any", "is_correct": False, "misconception": "Confusing quantifiers with how much/many"},
                            {"key": "D", "text": "any / some", "is_correct": False, "misconception": "Confusing quantifiers"}
                        ],
                        "accepted_text_answers": [
                            "many / much", "many much", "A"
                        ],
                        "pedagogical_success_reply": "برافو يا بطل! 💧 زجاجات المياه (bottles) تُعد فاستخدمنا many، والماء نفسه (water) لا يُعد فاستخدمنا much.",
                        "pedagogical_remediation_reply": "ركز يا بطل: كلمة bottles جمع معدود فنستخدم How many، أما water سائل غير معدود فنستخدم How much."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "Negative 'Some' Fallacy",
                        "answer": "We don't have some milk",
                        "expected_misconception": "Using 'some' in negative sentences instead of 'any'"
                    },
                    {
                        "title": "Pluralizing Uncountable ('waters')",
                        "answer": "many waters and milks",
                        "expected_misconception": "Pluralizing uncountable liquids with many"
                    }
                ]
            },
            {
                "concept_id": "c_comparatives_superlatives",
                "concept_name": "Comparatives & Superlatives",
                "arabic_title": "مقارنة وتفضيل الصفات",
                "mastery": 0.48,
                "stability": 2.8,
                "last_practiced": "2026-09-27",
                "course_evidence": (
                    "Short adjectives add -er than (faster than) and the + -est (the fastest). "
                    "Long adjectives use more/less + adjective + than, and the most/least. "
                    "Never say 'more faster'."
                ),
                "explanation_guide": (
                    "أكيد يا بطل! 🐆🐘 مقارنة وتفضيل الصفات سهلة جداً:\n\n"
                    "**1. المقارنة بين اثنين (Comparative):**\n"
                    "- الصفات القصيرة بنضيف لها: `er + than` (مثل: `faster than`, `taller than`).\n"
                    "- الصفات الطويلة بنستخدم: `more + adjective + than` (مثل: `more dangerous than`).\n"
                    "- ⚠️ انتبه: ممنوع نجمع الاتنين ونقول `more faster` ❌.\n\n"
                    "**2. التفضيل على الكل (Superlative):**\n"
                    "- لما نفضل واحد على كل المجموعة:\n"
                    "- الصفات القصيرة: `the + adjective + est` (مثل: `the fastest` الأسرع، `the highest` الأعلى).\n"
                    "- الصفات الطويلة: `the most + adjective` (مثل: `the most beautiful`)."
                ),
                "questions": [
                    {
                        "question_id": "q_comp_1",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "The cheetah is ______ animal on land, and it is ______ than a lion.",
                        "hint": "Fill in with the correct comparison forms of 'fast':",
                        "options": [
                            {"key": "A", "text": "the fastest / faster", "is_correct": True},
                            {"key": "B", "text": "the most fast / more fast", "is_correct": False, "misconception": "Using more/most with short adjectives"},
                            {"key": "C", "text": "the most fastest / more faster", "is_correct": False, "misconception": "Double comparative stacking"},
                            {"key": "D", "text": "faster / the fastest", "is_correct": False, "misconception": "Swapping comparative and superlative order"}
                        ],
                        "accepted_text_answers": [
                            "the fastest / faster", "fastest / faster", "the fastest and faster", "A"
                        ],
                        "pedagogical_success_reply": "برافو عليك! 🐆 إجابة نموذجية: the fastest للتفضيل على كل الحيوانات، و faster than للمقارنة بين الفهد والأسد.",
                        "pedagogical_remediation_reply": "خد بالك يا بطل! 💡 كلمة fast صفة قصيرة، في المقارنة بنحط لها er (faster than)، وفي التفضيل بنحط the + est (the fastest)، ومش بنستخدم معاها more أبداً."
                    },
                    {
                        "question_id": "q_comp_2",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "The blue whale is ______ creature in the entire world.",
                        "hint": "Superlative form of 'large':",
                        "options": [
                            {"key": "A", "text": "the largest", "is_correct": True},
                            {"key": "B", "text": "more large", "is_correct": False, "misconception": "Using more with short adjective"},
                            {"key": "C", "text": "larger than", "is_correct": False, "misconception": "Using comparative instead of superlative"},
                            {"key": "D", "text": "the most large", "is_correct": False, "misconception": "Using most with short adjective"}
                        ],
                        "accepted_text_answers": [
                            "the largest", "largest", "A"
                        ],
                        "pedagogical_success_reply": "إجابة صحيحة وممتازة! 🐋 الحوت الأزرق هو الأضخم في العالم كله (the largest).",
                        "pedagogical_remediation_reply": "فكر فيها يا بطل! 💡 احنا هنا بنفضل الحوت على كل كائنات العالم، والصفة large قصيرة فنقول the largest."
                    },
                    {
                        "question_id": "q_comp_3",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Mount Everest is ______ than Mount Catherine, but Everest is ______ mountain on Earth.",
                        "hint": "Comparing two, then comparing with all:",
                        "options": [
                            {"key": "A", "text": "higher / the highest", "is_correct": True},
                            {"key": "B", "text": "the highest / higher", "is_correct": False, "misconception": "Swapped order"},
                            {"key": "C", "text": "more high / most high", "is_correct": False, "misconception": "Using more/most with high"},
                            {"key": "D", "text": "higher / highest", "is_correct": False, "misconception": "Missing 'the' in superlative"}
                        ],
                        "accepted_text_answers": [
                            "higher / the highest", "higher the highest", "A"
                        ],
                        "pedagogical_success_reply": "عبقري! 🏔️ إيفرست أعلى من كاترين (higher than) وهو الأعلى على الإطلاق في كوكب الأرض (the highest).",
                        "pedagogical_remediation_reply": "خد بالك: مع than بنستخدم higher، ومع المقارنة بكل جبال الأرض بنحط the highest."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "Double Comparative ('more faster')",
                        "answer": "more faster than a lion",
                        "expected_misconception": "Combining 'more' with '-er' suffix on short adjectives"
                    }
                ]
            },
            {
                "concept_id": "c_egypt_ecosystems",
                "concept_name": "Ecosystems & Wildlife in Egypt",
                "arabic_title": "الأنظمة البيئية والحياة البرية في مصر",
                "mastery": 0.62,
                "stability": 4.5,
                "last_practiced": "2026-09-30",
                "course_evidence": (
                    "An ecosystem consists of living organisms (plants, animals) interacting with non-living elements (water, soil). "
                    "Red Sea mangrove trees protect shorelines from erosion and provide nurseries for marine life."
                ),
                "explanation_guide": (
                    "من عيوني يا بطل! 🌿🐢 الأنظمة البيئية والحياة البرية في مصر:\n\n"
                    "**1. ما هو النظام البيئي (Ecosystem)؟**\n"
                    "هو مجتمع طبيعي بيتكون من:\n"
                    "- **كائنات حية (Living things):** نباتات، حيوانات، طيور، وأسماك.\n"
                    "- **عناصر غير حية (Non-living things):** ماء، هواء، تربة، وشمس.\n"
                    "والاتنين بيتفاعلوا مع بعض عشان الحياة تستمر في توازن بيئي متكامل.\n\n"
                    "**2. أشجار المانجروف (Mangrove Trees) في البحر الأحمر:**\n"
                    "- بتعيش في المياه المالحة على السواحل.\n"
                    "- جذورها المتشابكة بتحمي الشواطئ من التآكل (Coastal erosion).\n"
                    "- بتعتبر حضانة طبيعية ومأوى آمن لصغار الأسماك والكائنات البحرية (Nursery for baby fish)."
                ),
                "questions": [
                    {
                        "question_id": "q_eco_1",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Why are mangrove trees along the Red Sea coast important?",
                        "hint": "Select the primary ecological benefit:",
                        "options": [
                            {"key": "A", "text": "They protect shores from erosion & shelter baby fish", "is_correct": True},
                            {"key": "B", "text": "They grow on dry desert mountains without water", "is_correct": False, "misconception": "Believing mangroves grow in dry deserts"},
                            {"key": "C", "text": "They are only used to make wooden furniture", "is_correct": False, "misconception": "Ignoring ecological nursery role"}
                        ],
                        "accepted_text_answers": [
                            "protect shores from erosion & shelter baby fish", "protect shores", "shelter baby fish", "A"
                        ],
                        "pedagogical_success_reply": "ممتاز جداً! 🌿 أشجار المانجروف بتحمي شواطئ البحر الأحمر وتعتبر بيتاً آمناً لصغار الأسماك والكائنات البحرية.",
                        "pedagogical_remediation_reply": "معلومة مهمة يا بطل: 🌊 أشجار المانجروف بتعيش في المياه المالحة على سواحل البحر الأحمر وجذورها بتمنع تآكل الشواطئ وتحمي الأسماك الصغيرة."
                    },
                    {
                        "question_id": "q_eco_2",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "Which of the following describes an ecosystem correctly?",
                        "hint": "An ecosystem includes two main parts:",
                        "options": [
                            {"key": "A", "text": "Living organisms and non-living things interacting together", "is_correct": True},
                            {"key": "B", "text": "Animals only living alone without plants or water", "is_correct": False, "misconception": "Excluding non-living elements"},
                            {"key": "C", "text": "Non-living rocks and sand without any living creatures", "is_correct": False, "misconception": "Excluding living elements"}
                        ],
                        "accepted_text_answers": [
                            "living organisms and non-living things interacting together", "living and non-living", "A"
                        ],
                        "pedagogical_success_reply": "أحسنت يا بطل! 🌍 النظام البيئي بيجمع بين الكائنات الحية (plants & animals) والعناصر غير الحية (water, soil, sun) في تفاعل مستمر.",
                        "pedagogical_remediation_reply": "ركز يا شاطر! 💡 النظام البيئي مش بس حيوانات، هو تفاعل بين الكائنات الحية والعناصر غير الحية زي الماء والتربة والشمس."
                    },
                    {
                        "question_id": "q_eco_3",
                        "question_type": "mcq",
                        "lang": "en",
                        "question_text": "The Nile River ecosystem provides freshwater and shelter for famous Egyptian wildlife such as the Nile ______.",
                        "hint": "Famous reptile living in Lake Nasser and the Nile:",
                        "options": [
                            {"key": "A", "text": "crocodile", "is_correct": True},
                            {"key": "B", "text": "polar bear", "is_correct": False, "misconception": "Choosing arctic animal"},
                            {"key": "C", "text": "penguin", "is_correct": False, "misconception": "Choosing antarctic animal"}
                        ],
                        "accepted_text_answers": [
                            "crocodile", "nile crocodile", "A"
                        ],
                        "pedagogical_success_reply": "إجابة صحيحة! 🐊 تمساح النيل (Nile crocodile) هو أحد أشهر الزواحف المائية في بيئة نهر النيل وبحيرة ناصر.",
                        "pedagogical_remediation_reply": "فكر فيها يا بطل: 💧 في نهر النيل الدافئ بيعيش تمساح النيل (Nile crocodile) مش الدب القطبي أو البطريق."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "Abiotic Exclusion Fallacy",
                        "answer": "Ecosystems only mean animals, plants and water are not important",
                        "expected_misconception": "Excluding non-living elements (water, soil) from ecosystem definitions"
                    }
                ]
            }
        ]
    },
    {
        "course_id": "MATH-501",
        "course_title": "الرياضيات — الصف الخامس",
        "code": "MATH-501",
        "lang": "ar",
        "description": "منهج الرياضيات الحديث: الكسور العشرية، العمليات الحسابية، جمع وطرح الكسور، ع.م.أ وم.م.أ.",
        "instructor": "أستاذ / محمد الشناوي (معلم خبير رياضيات)",
        "concepts": [
            {
                "concept_id": "c_decimals_place_value",
                "concept_name": "الكسور العشرية والقيمة المكانية",
                "arabic_title": "مقارنة الكسور العشرية والقيمة المكانية حتى الجزء من ألف",
                "mastery": 0.35,
                "stability": 2.0,
                "last_practiced": "2026-09-29",
                "course_evidence": (
                    "لمقارنة كسرين عشريين، نوازن أولاً عدد الخانات بوضع أصفار على اليمين. "
                    "مثال: 0.8 تكافئ 0.80 وهي أكبر من 0.25. لا يجوز مقارنة الأجزاء العشرية كأعداد صحيحة عادية."
                ),
                "explanation_guide": (
                    "أكيد يا بطل! تعال نبسطها بأسهل وأوضح طريقة في الدنيا: 💡\n\n"
                    "🪙 **طريقة الفلوس (أسهل طريقة تفهمك):**\n"
                    "- تخيل إن الـ 0.8 جنيه هي هي 0.80 يعني (80 قرش)! 🪙\n"
                    "- والـ 0.25 جنيه هي (25 قرش)! 🪙\n"
                    "مين أكبر؟ الـ 80 قرش طبعاً! عشان كده **0.8 > 0.25**.\n\n"
                    "📏 **القاعدة الرياضية الذهبية:**\n"
                    "1. عند مقارنة الأعداد العشرية، لازم نساوي عدد الخانات العشرية أولاً بوضع صفر على اليمين:\n"
                    "   الـ 0.8 تصبح 0.80.\n"
                    "2. بنقارن من الشمال لليمين خانة خانة:\n"
                    "   - الآحاد: 0 و 0 (متساويين).\n"
                    "   - خانة الجزء من عشرة: الأول فيه 8 والثاني فيه 2. وبما إن 8 أكبر من 2، يبقى الأول أكبر فوراً!\n\n"
                    "🏷️ **القيمة المكانية:**\n"
                    "- أول رقم بعد العلامة: (جزء من عشرة).\n"
                    "- ثاني رقم بعد العلامة: (جزء من مائة).\n"
                    "- ثالث رقم بعد العلامة: (جزء من ألف)."
                ),
                "questions": [
                    {
                        "question_id": "q_dec_1",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "قارن بين الكسرين العشريين: 0.8 و 0.25 مستخدماً العلامة المناسبة:",
                        "hint": "تذكر موازنة الخانات العشرية أولاً (0.8 = 0.80):",
                        "options": [
                            {"key": "A", "text": "0.8 > 0.25 (لأن 0.80 أكبر من 0.25)", "is_correct": True},
                            {"key": "B", "text": "0.8 < 0.25 (لأن 25 أكبر من 8)", "is_correct": False, "misconception": "مغالطة مقارنة العدد الصحيح: تجاهل القيمة المكانية"},
                            {"key": "C", "text": "0.8 = 0.25", "is_correct": False, "misconception": "اعتبار القيمتين متساويتين"}
                        ],
                        "accepted_text_answers": [
                            ">", "0.8 > 0.25", "0.8 اكبر من 0.25", "0.8 أكبر من 0.25", "0.8 أكبر", "أكبر", "اكبر",
                            "0.8 > 0.25 (لأن 0.80 أكبر من 0.25)", "A"
                        ],
                        "pedagogical_success_reply": "عبقري يا بطل! 🌟 0.8 فعلاً أكبر من 0.25 لأننا لما نساوي الخانات بتبقى 0.80 جزءاً من مائة وهي أكبر بكثير من 0.25.",
                        "pedagogical_remediation_reply": "خد بالك يا شاطر! 💡 في الكسور العشرية بنقارن الخانات من الشمال لليمين. 0.8 فيها 8 أجزاء من عشرة، بينما 0.25 فيها 2 جزء من عشرة فقط، عشان كده 0.8 > 0.25."
                    },
                    {
                        "question_id": "q_dec_2",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "القيمة المكانية للرقم 7 في العدد العشري 3.475 هي:",
                        "hint": "الرقم 4 في جزء من عشرة، فالرقم 7 يقع في:",
                        "options": [
                            {"key": "A", "text": "جزء من مائة (0.07)", "is_correct": True},
                            {"key": "B", "text": "جزء من عشرة (0.7)", "is_correct": False, "misconception": "الخلط بين الجزء من عشرة والجزء من مائة"},
                            {"key": "C", "text": "جزء من ألف (0.007)", "is_correct": False, "misconception": "الخلط مع الجزء من ألف"},
                            {"key": "D", "text": "عشرات (70)", "is_correct": False, "misconception": "الخلط بين الأجزاء العشرية والأعداد الصحيحة"}
                        ],
                        "accepted_text_answers": [
                            "جزء من مائة", "0.07", "جزء من مائه", "A"
                        ],
                        "pedagogical_success_reply": "ممتاز يا شاطر! 🎯 الرقم 7 هو ثاني رقم بعد العلامة العشرية، لذا قيمته المكانية هي 'جزء من مائة' وقيمته العددية 0.07.",
                        "pedagogical_remediation_reply": "ركز يا بطل! 💡 أول رقم بعد العلامة (4) جزء من عشرة، والرقم الثاني (7) هو جزء من مائة وقيمته 0.07."
                    },
                    {
                        "question_id": "q_dec_3",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "أي الأعداد العشرية التالية هو الأكبر قيمة: 0.65 أم 0.7 أم 0.599؟",
                        "hint": "ساوي الخانات العشرية أولاً: 0.650 و 0.700 و 0.599:",
                        "options": [
                            {"key": "A", "text": "0.7 (لأنه يساوي 0.700)", "is_correct": True},
                            {"key": "B", "text": "0.599 (لأن 599 أكبر من 7)", "is_correct": False, "misconception": "مغالطة مقارنة 599 مع 7 كأعداد صحيحة"},
                            {"key": "C", "text": "0.65", "is_correct": False, "misconception": "اعتبار 65 أكبر من 7"}
                        ],
                        "accepted_text_answers": [
                            "0.7", "0.700", "0.70", "A"
                        ],
                        "pedagogical_success_reply": "بطل حقيقي! 🏆 0.7 هي الأكبر لأننا لما نساوي الخانات العشرية تصبح 0.700 وهي أكبر من 0.650 وأكبر من 0.599.",
                        "pedagogical_remediation_reply": "خد بالك يا بطل! 💡 لو ساوينا الخانات بإضافة أصفار: الـ 0.7 تبقى 0.700، والـ 0.65 تبقى 0.650، يبقى طبعاً الـ 0.700 هي الأكبر!"
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "مغالطة مقارنة العدد الصحيح",
                        "answer": "0.25 أكبر من 0.8 لأن 25 أكبر من 8",
                        "expected_misconception": "تجاهل القيمة المكانية ومعاملة الأجزاء العشرية كأعداد صحيحة"
                    }
                ]
            },
            {
                "concept_id": "c_unlike_fractions",
                "concept_name": "جمع وطرح الكسور غير متحدة المقام",
                "arabic_title": "جمع وطرح الكسور بتوحيد المقامات",
                "mastery": 0.42,
                "stability": 2.6,
                "last_practiced": "2026-09-28",
                "course_evidence": (
                    "لجمع كسرين بمقامات مختلفة (1/2 + 1/3)، نوحد المقامات أولاً بإيجاد م.م.أ للمقامين (6)، "
                    "فيصبح 3/6 + 2/6 = 5/6. لا يجوز جمع المقامات إطلاقاً."
                ),
                "explanation_guide": (
                    "أهلاً يا بطل! 🍕 تعال نشوف إزاي نجمع ونطرح الكسور بسهولة تامة:\n\n"
                    "⚠️ **الخطأ الشائع القاتل:** إياك تجمع المقامات! يعني 1/2 + 1/3 مش بتطلع 2/5 أبداً ❌!\n\n"
                    "✅ **الخطوات الصحيحة بالترتيب:**\n"
                    "1. **توحيد المقامات:** نبحث عن المضاعف المشترك الأصغر (م.م.أ) للمقامين.\n"
                    "   - لمقام 2 و 3، المقام المشترك هو 6.\n"
                    "2. **تحويل البسط:**\n"
                    "   - الكسر الأول: (1/2) نضرب بسطاً ومقاماً في 3 فتصبح 3/6.\n"
                    "   - الكسر الثاني: (1/3) نضرب بسطاً ومقاماً في 2 فتصبح 2/6.\n"
                    "3. **الجمع أو الطرح:** نثبت المقام (6) ونجمع البسطين:\n"
                    "   - 3/6 + 2/6 = **5/6**! 🎉"
                ),
                "questions": [
                    {
                        "question_id": "q_frac_1",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "أوجد ناتج جمع: 1/2 + 1/3 في أبسط صورة:",
                        "hint": "المقام المشترك للعددين 2 و 3 هو 6:",
                        "options": [
                            {"key": "A", "text": "5/6 (بعد توحيد المقامات على 6)", "is_correct": True},
                            {"key": "B", "text": "2/5 (بجمع البسط مع البسط والمقام مع المقام)", "is_correct": False, "misconception": "جمع المقامات خطأ شائع"},
                            {"key": "C", "text": "1/6", "is_correct": False, "misconception": "طرح بدلاً من الجمع"},
                            {"key": "D", "text": "3/5", "is_correct": False, "misconception": "تخمين عشوائي"}
                        ],
                        "accepted_text_answers": [
                            "5/6", "خمسة أسداس", "5 / 6", "A"
                        ],
                        "pedagogical_success_reply": "ممتاز جداً! 🍰 وحدت المقامات على 6: (3/6 + 2/6 = 5/6) دون الوقوع في فخ جمع المقامات.",
                        "pedagogical_remediation_reply": "انتبه يا بطل! 💡 المقامات لا تُجمع أبداً. نوحد المقامات أولاً على 6: النصف = 3/6 والثلث = 2/6، ومجموعهما 5/6."
                    },
                    {
                        "question_id": "q_frac_2",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "ما هو المقام المشترك الأصغر (م.م.أ) المناسب لجمع الكسرين 1/4 و 2/5؟",
                        "hint": "مضاعفات العدد 4 والعدد 5:",
                        "options": [
                            {"key": "A", "text": "20", "is_correct": True},
                            {"key": "B", "text": "9 (بجمع 4 + 5)", "is_correct": False, "misconception": "جمع المقامات بدلاً من إيجاد م.م.أ"},
                            {"key": "C", "text": "10", "is_correct": False, "misconception": "مضاعف لـ 5 وليس لـ 4"},
                            {"key": "D", "text": "40", "is_correct": False, "misconception": "مضاعف مشترك ولكنه ليس الأصغر"}
                        ],
                        "accepted_text_answers": [
                            "20", "عشرون", "A"
                        ],
                        "pedagogical_success_reply": "إجابة دقيقة! 🎯 أصغر مضاعف مشترك يقبل القسمة على 4 و 5 في نفس الوقت هو 20.",
                        "pedagogical_remediation_reply": "فكر فيها يا بطل: 💡 مضاعفات 4 هي (4, 8, 12, 16, 20...) ومضاعفات 5 هي (5, 10, 15, 20...). أول رقم مشترك هو 20."
                    },
                    {
                        "question_id": "q_frac_3",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "أوجد ناتج طرح الكسرين: 3/4 - 1/2 =",
                        "hint": "حول 1/2 إلى كسر مقامه 4:",
                        "options": [
                            {"key": "A", "text": "1/4 (لأن 1/2 تكافئ 2/4 و 3/4 - 2/4 = 1/4)", "is_correct": True},
                            {"key": "B", "text": "2/2 = 1", "is_correct": False, "misconception": "طرح المقامات"},
                            {"key": "C", "text": "2/4 دون تبسيط", "is_correct": False, "misconception": "حساب خاطئ"},
                            {"key": "D", "text": "1/8", "is_correct": False, "misconception": "ضرب المقامات"}
                        ],
                        "accepted_text_answers": [
                            "1/4", "ربع", "1 / 4", "A"
                        ],
                        "pedagogical_success_reply": "رائع يا بطل! 🌟 حولت النصف إلى 2/4، ثم طرحت: 3/4 - 2/4 = 1/4 بكل إتقان.",
                        "pedagogical_remediation_reply": "خد بالك: النصف (1/2) بيساوي (2/4). دلوقتي نطرح البسط: 3 - 2 = 1 والمقام ثابت 4، فالناتج 1/4."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "مغالطة جمع المقامات",
                        "answer": "1/2 + 1/3 = 2/5",
                        "expected_misconception": "جمع البسط مع البسط والمقام مع المقام مباشرة"
                    }
                ]
            },
            {
                "concept_id": "c_decimal_mult_div",
                "concept_name": "ضرب وقسمة الكسور العشرية في 10 و 100",
                "arabic_title": "تحريك العلامة العشرية بالضرب والقسمة",
                "mastery": 0.50,
                "stability": 3.1,
                "last_practiced": "2026-09-30",
                "course_evidence": (
                    "عند الضرب في 10 أو 100، تتحرك العلامة لليمين بعدد الأصفار (4.75 × 100 = 475). "
                    "عند القسمة على 10، تتحرك العلامة لليسار بعدد الأصفار (35.8 ÷ 10 = 3.58)."
                ),
                "explanation_guide": (
                    "أهلاً يا عبقري! ✖️➗ قاعدة حركة العلامة العشرية دي لعبة سحرية ممتعة:\n\n"
                    "**1. الضرب (✖️):** الضرب بيكبّر العدد! عشان كده بنحرّك العلامة **ناحية اليمين** بعدد أصفار العدد:\n"
                    "- في 10: نحرك العلامة خطوة واحدة لليمين (4.75 × 10 = 47.5).\n"
                    "- في 100: نحرك العلامة خطوتين لليمين (4.75 × 100 = 475).\n"
                    "- في 1000: نحرك العلامة 3 خطوات لليمين.\n\n"
                    "**2. القسمة (➗):** القسمة بتصغّر العدد! عشان كده بنحرّك العلامة **ناحية اليسار**:\n"
                    "- في 10: نحرك العلامة خطوة واحدة لليسار (35.8 ÷ 10 = 3.58).\n"
                    "- في 100: نحرك العلامة خطوتين لليسار."
                ),
                "questions": [
                    {
                        "question_id": "q_mult_1",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "أوجد ناتج العملية التالية: 4.75 × 100 =",
                        "hint": "الضرب في 100 يحرك العلامة خطوتين لليمين:",
                        "options": [
                            {"key": "A", "text": "475 (تحريك العلامة خانتين لليمين)", "is_correct": True},
                            {"key": "B", "text": "47.5 (تحريك خانة واحدة فقط)", "is_correct": False, "misconception": "الضرب في 10 بدلاً من 100"},
                            {"key": "C", "text": "0.0475 (تحريك لليسار كأنه قسمة)", "is_correct": False, "misconception": "الخلط بين الضرب والقسمة"},
                            {"key": "D", "text": "4750", "is_correct": False, "misconception": "إضافة أصفار دون حساب الخانات"}
                        ],
                        "accepted_text_answers": [
                            "475", "أربعمائة وخمسة وسبعون", "A"
                        ],
                        "pedagogical_success_reply": "إجابة صحيحة وسريعة! 🚀 عند الضرب في 100 قفزت العلامة العشرية خطوتين لليمين فأصبح العدد 475.",
                        "pedagogical_remediation_reply": "تذكر يا بطل: 💡 الضرب في 100 يحرك العلامة خطوتين جهة اليمين، فتعدي الـ 7 والـ 5 وتختفي ليصبح الناتج 475."
                    },
                    {
                        "question_id": "q_mult_2",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "أوجد ناتج العملية التالية: 35.8 ÷ 10 =",
                        "hint": "القسمة تصغر العدد وتحرك العلامة خطوة لليسار:",
                        "options": [
                            {"key": "A", "text": "3.58 (تحريك العلامة خانة واحدة لليسار)", "is_correct": True},
                            {"key": "B", "text": "358 (تحريك لليمين كأنه ضرب)", "is_correct": False, "misconception": "الخلط بين القسمة والضرب"},
                            {"key": "C", "text": "0.358", "is_correct": False, "misconception": "القسمة على 100"},
                            {"key": "D", "text": "35.08", "is_correct": False, "misconception": "وضع الصفر في غير محله"}
                        ],
                        "accepted_text_answers": [
                            "3.58", "A"
                        ],
                        "pedagogical_success_reply": "برافو يا شاطر! 👏 القسمة على 10 حركت العلامة خطوة واحدة لليسار بين الـ 3 والـ 5 فصار 3.58.",
                        "pedagogical_remediation_reply": "ركز يا بطل: 💡 في القسمة على 10 بنحرك العلامة خطوة واحدة جهة اليسار (35.8 ➔ 3.58)."
                    },
                    {
                        "question_id": "q_mult_3",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "إذا ضربنا العدد العشري 0.6 في 1000، فإن الناتج يكون:",
                        "hint": "حرك العلامة 3 خطوات لليمين، وزود أصفار للخطوات الفارغة:",
                        "options": [
                            {"key": "A", "text": "600 (تحريك 3 خطوات لليمين بإضافة صفرين)", "is_correct": True},
                            {"key": "B", "text": "60", "is_correct": False, "misconception": "الضرب في 100 فقط"},
                            {"key": "C", "text": "6", "is_correct": False, "misconception": "الضرب في 10 فقط"},
                            {"key": "D", "text": "0.0006", "is_correct": False, "misconception": "قسمة بدلاً من ضرب"}
                        ],
                        "accepted_text_answers": [
                            "600", "ستمائة", "A"
                        ],
                        "pedagogical_success_reply": "ممتاز يا بطل! 🌟 حركت العلامة 3 خطوات لليمين: خطوة عدت الـ 6، والخطوتين الباقيتين وضعنا بدلهما صفرين ليصبح 600.",
                        "pedagogical_remediation_reply": "خد بالك: الـ 1000 فيها 3 أصفار. العلامة تعدي الـ 6 (خطوة)، ونحط صفرين للخطوتين التانيين فتصبح 600."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "عكس اتجاه العلامة في الضرب",
                        "answer": "4.75 × 100 = 0.0475",
                        "expected_misconception": "تحريك العلامة لليسار أثناء الضرب بدلاً من اليمين"
                    }
                ]
            },
            {
                "concept_id": "c_gcf_lcm",
                "concept_name": "العوامل والمضاعفات (ع.م.أ و م.م.أ)",
                "arabic_title": "العامل المشترك الأكبر والمضاعف المشترك الأصغر",
                "mastery": 0.38,
                "stability": 2.2,
                "last_practiced": "2026-09-29",
                "course_evidence": (
                    "للعددين 6 و 8: ع.م.أ = 2 (أكبر قاسم مشترك). "
                    "م.م.أ = 24 (أصغر مضاعف مشترك يقبل القسمة عليهما معاً). "
                    "العدد 2 هو العدد الأولي الزوجي الوحيد."
                ),
                "explanation_guide": (
                    "من عيوني يا بطل! 🔢 تعال نفرق بين العامل والمضاعف بكل بساطة:\n\n"
                    "**1. العامل المشترك الأكبر (ع.م.أ):**\n"
                    "- هو **أكبر عدد يقبل عليه العددان القسمة معاً** بدون باقٍ.\n"
                    "- دايماً بيكون أصغر من أو يساوي أصغر العددين.\n"
                    "- مثال: للعددين 6 و 8، عوامل 6 هي (1, 2, 3, 6) وعوامل 8 هي (1, 2, 4, 8) ➔ إذن ع.م.أ = **2**.\n\n"
                    "**2. المضاعف المشترك الأصغر (م.م.أ):**\n"
                    "- هو **أصغر عدد يقبل القسمة على العددين معاً** (مضاعفاتهم المشتركة).\n"
                    "- مضاعفات 6: (0, 6, 12, 18, **24**, 30...)\n"
                    "- مضاعفات 8: (0, 8, 16, **24**, 32...)\n"
                    "- أول مضاعف مشترك بعد الصفر هو **24**!\n\n"
                    "⭐ **معلومات ذهبية للامتحان:**\n"
                    "- العدد الأولي الزوجي الوحيد هو: **2**.\n"
                    "- العامل المشترك لجميع الأعداد هو: **1**.\n"
                    "- المضاعف المشترك لجميع الأعداد هو: **0**."
                ),
                "questions": [
                    {
                        "question_id": "q_gcf_1",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "العددان 6 و 8: ما هو العامل المشترك الأكبر (ع.م.أ) والمضاعف المشترك الأصغر (م.م.أ) لهما؟",
                        "hint": "عوامل 6 و 8 المشتركة، ومضاعفات 6 و 8 المشتركة:",
                        "options": [
                            {"key": "A", "text": "ع.م.أ = 2 و م.م.أ = 24", "is_correct": True},
                            {"key": "B", "text": "ع.م.أ = 24 و م.م.أ = 2", "is_correct": False, "misconception": "الخلط بين العامل والمضاعف"},
                            {"key": "C", "text": "ع.م.أ = 1 و م.م.أ = 48", "is_correct": False, "misconception": "ضرب العددين دون تبسيط"},
                            {"key": "D", "text": "ع.م.أ = 4 و م.م.أ = 16", "is_correct": False, "misconception": "حساب غير دقيق"}
                        ],
                        "accepted_text_answers": [
                            "ع.م.أ = 2 و م.م.أ = 24", "2 و 24", "2", "24", "A"
                        ],
                        "pedagogical_success_reply": "إجابة عبقرية! 🌟 ع.م.أ هو 2 (أكبر قاسم مشترك)، وم.م.أ هو 24 (أصغر مضاعف مشترك للعددين 6 و 8).",
                        "pedagogical_remediation_reply": "خد بالك يا بطل: 💡 العامل (ع.م.أ) دايماً صغير (الـ 6 والـ 8 يقبلوا القسمة على 2)، بينما المضاعف (م.م.أ) كبير (الـ 24 بتقبل القسمة على 6 و 8)."
                    },
                    {
                        "question_id": "q_gcf_2",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "العدد الأولي الزوجي الوحيد هو:",
                        "hint": "العدد الأولي يقبل القسمة على نفسه وعلى 1 فقط:",
                        "options": [
                            {"key": "A", "text": "2 (لأنه يقبل القسمة على نفسه و 1 فقط)", "is_correct": True},
                            {"key": "B", "text": "4", "is_correct": False, "misconception": "العدد 4 يقبل على 2 فليس أولياً"},
                            {"key": "C", "text": "0", "is_correct": False, "misconception": "الصفر ليس عدداً أولياً"},
                            {"key": "D", "text": "1", "is_correct": False, "misconception": "الواحد له عامل واحد فقط فليس أولياً"}
                        ],
                        "accepted_text_answers": [
                            "2", "اثنان", "A"
                        ],
                        "pedagogical_success_reply": "برافو! 🎯 العدد 2 هو بالفعل العدد الأولي الزوجي الوحيد، وكل باقي الأعداد الأولية فردية.",
                        "pedagogical_remediation_reply": "معلومة ذهبية يا بطل: 💡 أي عدد زوجي تاني زي 4 أو 6 بيقبل القسمة على 2، عشان كده 2 هو العدد الأولي الزوجي الوحيد!"
                    },
                    {
                        "question_id": "q_gcf_3",
                        "question_type": "mcq",
                        "lang": "ar",
                        "question_text": "العامل المشترك لجميع الأعداد الصحيحة هو:",
                        "hint": "كل الأعداد تقبل القسمة على:",
                        "options": [
                            {"key": "A", "text": "1 (الواحد الصحيح)", "is_correct": True},
                            {"key": "B", "text": "0 (الصفر)", "is_correct": False, "misconception": "القسمة على الصفر غير معرفة"},
                            {"key": "C", "text": "2", "is_correct": False, "misconception": "عامل للأعداد الزوجية فقط"},
                            {"key": "D", "text": "10", "is_correct": False, "misconception": "عامل للأعداد التي تبدأ بصفر"}
                        ],
                        "accepted_text_answers": [
                            "1", "واحد", "الواحد الصحيح", "A"
                        ],
                        "pedagogical_success_reply": "أحسنت! 🥇 العدد 1 هو العامل المشترك لجميع الأعداد لأن أي عدد يقبل القسمة على 1.",
                        "pedagogical_remediation_reply": "تذكر يا بطل: 💡 أي عدد في الدنيا يقبل القسمة على 1 (العامل المشترك)، بينما 0 هو المضاعف المشترك لجميع الأعداد."
                    }
                ],
                "misconception_presets": [
                    {
                        "title": "الخلط بين العامل والمضاعف",
                        "answer": "ع.م.أ = 24 و م.م.أ = 2",
                        "expected_misconception": "عكس مفهوم العامل والمضاعف"
                    }
                ]
            }
        ]
    }
]

# Ensure backward compatibility: populate sample_question from questions[0]
for course in COURSES_DATA:
    for concept in course["concepts"]:
        if "questions" in concept and len(concept["questions"]) > 0:
            concept["sample_question"] = concept["questions"][0]
