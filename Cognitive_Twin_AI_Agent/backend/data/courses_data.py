"""
SALI — Primary 5 Courses Data (Egyptian Curriculum)
Provides 2 accredited Primary 5 (الصف الخامس الابتدائي) courses:
1. English (Connect 5) — Grammar, Quantifiers, Adjectives, Ecosystems
2. Mathematics (الرياضيات) — Decimals, Unlike Fractions, Operations, GCF/LCM
Includes calibrated misconceptions, sample questions, and pedagogical evidence.
"""

STUDENT_PROFILE = {
    "student_id": "STD-PRI5-104",
    "name": "كريم عز الدين (Kareem)",
    "email": "kareem.grade5@sali-learning.eg",
    "degree": "Primary 5 (Grade 5) — الصف الخامس الابتدائي",
    "semester": "Term 1, Academic Year 2026/2027",
    "overall_cognitive_index": 0.68,
    "current_streak_days": 6,
    "memory_stability_days": 3.8
}

COURSES_DATA = [
    {
        "course_id": "ENG-501",
        "course_title": "English — Connect 5 (Primary 5)",
        "code": "ENG-501",
        "description": "Ministry of Education Connect 5 curriculum: Past Simple, Quantifiers, Adjectives, and Egyptian Ecosystems.",
        "instructor": "Teacher / مستر أحمد فاروق",
        "concepts": [
            {
                "concept_id": "c_past_simple",
                "concept_name": "Past Simple & Irregular Verbs",
                "mastery": 0.40,
                "stability": 2.2,
                "last_practiced": "2026-09-28",
                "course_evidence": (
                    "In Connect 5 Unit 1, we use the Past Simple tense to talk about actions finished in the past. "
                    "Regular verbs add -ed (visited, played, cooked). Irregular verbs change completely and NEVER take -ed "
                    "(go -> went, see -> saw, buy -> bought, have -> had). "
                    "In negative sentences, we use 'didn't' followed by the infinitive base verb (e.g., 'He didn't go', NOT 'didn't went')."
                ),
                "sample_question": {
                    "question_id": "q_eng_01",
                    "question_text": "Yesterday, my family and I ______ to Alexandria and we ______ the Qaitbay Citadel.",
                    "correct_answer": "went / visited (because 'go' is irregular and changes to 'went', while 'visit' is regular and takes '-ed')",
                    "misconception_presets": [
                        {
                            "title": "Over-regularization Fallacy ('goed')",
                            "answer": "goed / visited because all past verbs must end with -ed",
                            "expected_misconception": "Applying regular -ed rule to irregular verbs like 'go'"
                        },
                        {
                            "title": "Double Past Tense Fallacy ('didn't went')",
                            "answer": "We didn't went because both words must be in the past tense",
                            "expected_misconception": "Using past form after auxiliary 'didn't' instead of base infinitive"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_nouns_quantifiers",
                "concept_name": "Countable / Uncountable & Some / Any",
                "mastery": 0.55,
                "stability": 3.4,
                "last_practiced": "2026-09-29",
                "course_evidence": (
                    "In Connect 5 Unit 2 (At the Market), countable nouns have a singular and plural form (an apple, three apples). "
                    "Uncountable nouns cannot be counted and have NO plural form (water, milk, rice, money). "
                    "We use 'many' with countable nouns and 'much' with uncountable nouns. "
                    "We use 'some' in affirmative sentences ('I have some rice') and polite offers ('Would you like some tea?'), "
                    "and 'any' in negative sentences ('We don't have any milk') and questions."
                ),
                "sample_question": {
                    "question_id": "q_eng_02",
                    "question_text": "Choose the correct words: We don't have ______ milk in the fridge, but there are ______ fresh apples.",
                    "correct_answer": "any / some (use 'any' in negative sentences and 'some' in positive sentences with plural nouns)",
                    "misconception_presets": [
                        {
                            "title": "Pluralizing Uncountable Fallacy ('many waters')",
                            "answer": "There are many waters and milks in the fridge",
                            "expected_misconception": "Treating liquids and uncountable nouns as countable plurals with 'many'"
                        },
                        {
                            "title": "Negative 'Some' Fallacy",
                            "answer": "We don't have some milk because some means a small quantity",
                            "expected_misconception": "Using 'some' in negative clauses instead of 'any'"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_comparatives_superlatives",
                "concept_name": "Comparatives & Superlatives",
                "mastery": 0.48,
                "stability": 2.8,
                "last_practiced": "2026-09-27",
                "course_evidence": (
                    "In Connect 5 Unit 3, for short adjectives (one syllable), we add -er + than for comparison (fast -> faster than, big -> bigger than) "
                    "and the + -est for superlatives (the fastest, the biggest). For long adjectives with two or more syllables, "
                    "we use 'more / less + adjective + than' (more dangerous than) and 'the most / least' (the most dangerous). "
                    "We NEVER combine 'more' with '-er' (e.g. 'more faster' is strictly incorrect)."
                ),
                "sample_question": {
                    "question_id": "q_eng_03",
                    "question_text": "The cheetah is ______ (fast) land animal, and it is ______ (fast) than a lion.",
                    "correct_answer": "the fastest / faster than",
                    "misconception_presets": [
                        {
                            "title": "Double Comparative Fallacy ('more faster')",
                            "answer": "The cheetah is the most fastest and it is more faster than a lion",
                            "expected_misconception": "Stacking 'more' or 'most' on top of short adjective suffixes -er/-est"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_egypt_ecosystems",
                "concept_name": "Ecosystems & Egyptian Wildlife",
                "mastery": 0.62,
                "stability": 4.5,
                "last_practiced": "2026-09-30",
                "course_evidence": (
                    "An ecosystem is a community where living things (plants, animals) interact with non-living elements (water, soil, sunlight). "
                    "In Egypt, coastal mangrove trees along the Red Sea protect shorelines from storms and erosion while providing a safe habitat "
                    "for young fish and crabs. The Nile River ecosystem supports rich soil and wetland biodiversity."
                ),
                "sample_question": {
                    "question_id": "q_eng_04",
                    "question_text": "Why are mangrove trees in Egypt vital for the Red Sea marine ecosystem?",
                    "correct_answer": "They prevent coastal erosion and provide a protected nursery shelter for baby marine organisms",
                    "misconception_presets": [
                        {
                            "title": "Abiotic Exclusion Fallacy",
                            "answer": "Ecosystems only mean wild animals living together, water and rocks do not matter",
                            "expected_misconception": "Excluding abiotic factors (soil, water, climate) from the ecosystem concept"
                        }
                    ]
                }
            }
        ]
    },
    {
        "course_id": "MATH-501",
        "course_title": "الرياضيات — الصف الخامس الابتدائي",
        "code": "MATH-501",
        "description": "منهج وزارة التربية والتعليم الجديد: الكسور العشرية، جمع وطرح الكسور الاعتيادية، والعمليات الحسابية وع.م.أ وم.م.أ.",
        "instructor": "أستاذ / محمد الشناوي (معلم خبير رياضيات)",
        "concepts": [
            {
                "concept_id": "c_decimals_place_value",
                "concept_name": "الكسور العشرية والقيمة المكانية حتى الجزء من ألف",
                "mastery": 0.35,
                "stability": 2.0,
                "last_practiced": "2026-09-29",
                "course_evidence": (
                    "يتكون الكسر العشري من عدد صحيح وعلامة عشرية وأجزاء: جزء من عشرة (Tenths)، جزء من مائة (Hundredths)، وجزء من ألف (Thousandths). "
                    "لمقارنة كسرين عشريين، نقارن أولاً العدد الصحيح، ثم الأجزاء من اليسار إلى اليمين بعد موازنة عدد الخانات بوضع أصفار على اليمين. "
                    "مثال: 0.8 = 0.800 وهي أكبر من 0.250 لأن 8 أجزاء من عشرة أكبر من جزءين من عشرة."
                ),
                "sample_question": {
                    "question_id": "q_math_01",
                    "question_text": "قارن بين العددين العشريين: 0.8 و 0.25 مستخدماً العلامة المناسبة (> أو < أو =).",
                    "correct_answer": "0.8 > 0.25 لأن 0.8 تكافئ 0.80 جزءاً من مائة وهي أكبر من 0.25",
                    "misconception_presets": [
                        {
                            "title": "مغالطة مقارنة العدد الصحيح (Whole-Number Fallacy)",
                            "answer": "0.25 أكبر من 0.8 لأن العدد 25 أكبر من العدد 8",
                            "expected_misconception": "تجاهل القيمة المكانية ومعاملة الأجزاء العشرية كأعداد صحيحة عادية"
                        },
                        {
                            "title": "مغالطة عدد الخانات",
                            "answer": "0.25 أكبر لأنها مكونة من رقمين بينما 0.8 مكونة من رقم واحد فقط",
                            "expected_misconception": "الاعتقاد بأن الكسر العشري ذو الأرقام الأكثر يكون هو الأكبر دائماً"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_unlike_fractions",
                "concept_name": "جمع وطرح الكسور غير متحدة المقام",
                "mastery": 0.42,
                "stability": 2.6,
                "last_practiced": "2026-09-28",
                "course_evidence": (
                    "لجمع أو طرح كسرين اعتياديين بمقامات مختلفة، يجب أولاً إيجاد المضاعف المشترك الأصغر للمقامين (م.م.أ) لتوحيد المقامات، "
                    "ثم نجمع أو نطرح البسطين مع بقاء المقام الموحد ثابتاً كما هو دون تغيير. لا يجوز إطلاقاً جمع أو طرح المقامات. "
                    "مثال: 1/2 + 1/3 = 3/6 + 2/6 = 5/6."
                ),
                "sample_question": {
                    "question_id": "q_math_02",
                    "question_text": "احسب ناتج: 1/2 + 1/3 في أبسط صورة.",
                    "correct_answer": "5/6 بعد توحيد المقامات على 6 (3/6 + 2/6 = 5/6)",
                    "misconception_presets": [
                        {
                            "title": "مغالطة جمع المقامات (Across-Addition Fallacy)",
                            "answer": "الناتج 2/5 بجمع البسط 1+1=2 وجمع المقام 2+3=5",
                            "expected_misconception": "جمع البسط مع البسط والمقام مع المقام مباشرة دون توحيد المقامات"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_decimal_mult_div",
                "concept_name": "ضرب وقسمة الأعداد العشرية في قوى العدد 10",
                "mastery": 0.50,
                "stability": 3.1,
                "last_practiced": "2026-09-30",
                "course_evidence": (
                    "عند ضرب كسر عشري في 10 أو 100 أو 1000، تتحرك العلامة العشرية جهة اليمين بعدد أصفار المضاعف (3.45 × 10 = 34.5). "
                    "وعند القسمة على 10 أو 100 أو 1000، تتحرك العلامة العشرية جهة اليسار (25.8 ÷ 10 = 2.58). "
                    "الضرب في 0.1 يعادل تماماً القسمة على 10."
                ),
                "sample_question": {
                    "question_id": "q_math_03",
                    "question_text": "ما هو ناتج: 4.75 × 100 ؟",
                    "correct_answer": "475 (تتحرك العلامة العشرية خانتين إلى اليمين)",
                    "misconception_presets": [
                        {
                            "title": "مغالطة اتجاه حركة العلامة العشرية",
                            "answer": "0.0475 بتحريك العلامة جهة اليسار لأن الضرب يصغر الرقم",
                            "expected_misconception": "الخلط بين اتجاه حركة العلامة في الضرب (يميناً) والقسمة (يساراً)"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_gcf_lcm",
                "concept_name": "العوامل والمضاعفات (ع.م.أ و م.م.أ)",
                "mastery": 0.38,
                "stability": 2.3,
                "last_practiced": "2026-09-27",
                "course_evidence": (
                    "العامل المشترك الأكبر (ع.م.أ) هو أكبر عدد يقسم كلا العددين معاً، ونستخرجه بضرب العوامل الأولية المشتركة فقط. "
                    "المضاعف المشترك الأصغر (م.م.أ) هو أصغر عدد يقبل القسمة على كلا العددين، ونستخرجه بضرب جميع العوامل الأولية المشتركة وغير المشتركة. "
                    "للعددين 6 (2×3) و 8 (2×2×2): ع.م.أ = 2، بينما م.م.أ = 2×3×2×2 = 24."
                ),
                "sample_question": {
                    "question_id": "q_math_04",
                    "question_text": "أوجد العامل المشترك الأكبر (ع.م.أ) والمضاعف المشترك الأصغر (م.م.أ) للعددين 6 و 8.",
                    "correct_answer": "ع.م.أ = 2 ، و م.م.أ = 24",
                    "misconception_presets": [
                        {
                            "title": "مغالطة التبديل بين العامل والمضاعف",
                            "answer": "ع.م.أ = 24 و م.م.أ = 2",
                            "expected_misconception": "عكس مفهوم العامل والمضاعف بسبب كلمة 'الأكبر' و 'الأصغر'"
                        },
                        {
                            "title": "مغالطة الضرب المباشر للمضاعف",
                            "answer": "م.م.أ هو حاصل ضرب 6 × 8 = 48 دائماً",
                            "expected_misconception": "إهمال العوامل الأولية المشتركة وافتراض أن م.م.أ دائماً ضرب العددين"
                        }
                    ]
                }
            }
        ]
    }
]
