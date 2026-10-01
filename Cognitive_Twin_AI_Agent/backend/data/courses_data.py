"""
SALI — Primary 5 Courses Data (Egyptian Curriculum)
Richly structured for Primary 5 (الصف الخامس الابتدائي):
- Connect 5 (English)
- Mathematics (الرياضيات)
Includes question options (MCQ), accepted variants, and friendly pedagogical feedback.
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
                "sample_question": {
                    "question_id": "q_eng_01",
                    "question_type": "mcq_or_fill",
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
                    "pedagogical_remediation_reply": "خد بالك يا بطل! 💡 في الماضي البسيط: الفعل go غير منتظم وماضيه went (مش بنحط له ed)، بينما visit و travel أفعال منتظمة بنضيف لها ed.",
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
                }
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
                "sample_question": {
                    "question_id": "q_eng_02",
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
                    "pedagogical_remediation_reply": "ركز يا بطل! 💡 في الجمل المنفية (don't have) بنستخدم 'any'، أما في الجمل المثبتة بنستخدم 'some'.",
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
                }
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
                "sample_question": {
                    "question_id": "q_eng_03",
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
                    "pedagogical_success_reply": "برافو عليك! 🐆 إجابة نموذجية: the fastest للتفضيل و faster than للمقارنة بين حيوانين.",
                    "pedagogical_remediation_reply": "خد بالك يا بطل! 💡 كلمة fast صفة قصيرة، في المقارنة بنحط لها er (faster than)، وفي التفضيل بنحط the + est (the fastest)، ومش بنستخدم معاها more أبداً.",
                    "misconception_presets": [
                        {
                            "title": "Double Comparative ('more faster')",
                            "answer": "more faster than a lion",
                            "expected_misconception": "Combining 'more' with '-er' suffix on short adjectives"
                        }
                    ]
                }
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
                "sample_question": {
                    "question_id": "q_eng_04",
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
                    "pedagogical_remediation_reply": "معلومة مهمة يا بطل: 🌊 أشجار المانجروف بتعيش في المياه المالحة على سواحل البحر الأحمر وجذورها بتمنع تآكل الشواطئ وتحمي الأسماك الصغيرة.",
                    "misconception_presets": [
                        {
                            "title": "Abiotic Exclusion Fallacy",
                            "answer": "Ecosystems only mean animals, plants and water are not important",
                            "expected_misconception": "Excluding non-living elements (water, soil) from ecosystem definitions"
                        }
                    ]
                }
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
                "sample_question": {
                    "question_id": "q_math_01",
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
                    "pedagogical_remediation_reply": "خد بالك يا شاطر! 💡 في الكسور العشرية بنقارن الخانات من الشمال لليمين. 0.8 فيها 8 أجزاء من عشرة، بينما 0.25 فيها 2 جزء من عشرة فقط، عشان كده 0.8 > 0.25.",
                    "misconception_presets": [
                        {
                            "title": "مغالطة مقارنة العدد الصحيح",
                            "answer": "0.25 أكبر من 0.8 لأن 25 أكبر من 8",
                            "expected_misconception": "تجاهل القيمة المكانية ومعاملة الأجزاء العشرية كأعداد صحيحة"
                        }
                    ]
                }
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
                "sample_question": {
                    "question_id": "q_math_02",
                    "question_type": "mcq",
                    "lang": "ar",
                    "question_text": "احسب ناتج: 1/2 + 1/3 في أبسط صورة:",
                    "hint": "أوجد م.م.أ للعددين 2 و 3 ووحد المقامات:",
                    "options": [
                        {"key": "A", "text": "5/6 (بعد توحيد المقامات على 6)", "is_correct": True},
                        {"key": "B", "text": "2/5 (بجمع 1+1 على 2+3)", "is_correct": False, "misconception": "مغالطة جمع المقامات مباشرة"},
                        {"key": "C", "text": "2/6", "is_correct": False, "misconception": "خطأ في ضرب البسط"},
                        {"key": "D", "text": "1/6", "is_correct": False, "misconception": "إجراء عملية طرح بدلاً من الجمع"}
                    ],
                    "accepted_text_answers": [
                        "5/6", "خمسة أسداس", "خمسة على ستة", "5 / 6", "A"
                    ],
                    "pedagogical_success_reply": "برافو عليك يا فنان! 👏 وحدت المقامات على 6: النصف = 3/6 والثلث = 2/6، ومجموعهم 5/6، ممتاز إنك لم تجمع المقامات!",
                    "pedagogical_remediation_reply": "تنبيه مهم جداً يا بطل! ⚠️ في الكسور مش بنجمع المقامات أبداً! لازم أولاً نوحد المقامات: م.م.أ للـ 2 والـ 3 هو 6. (3/6 + 2/6 = 5/6).",
                    "misconception_presets": [
                        {
                            "title": "مغالطة جمع المقامات (1/2 + 1/3 = 2/5)",
                            "answer": "الناتج 2/5 بجمع البسط 1+1 والمقام 2+3",
                            "expected_misconception": "جمع البسط مع البسط والمقام مع المقام مباشرة"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_decimal_mult_div",
                "concept_name": "ضرب وقسمة الكسور العشرية في 10 و 100",
                "arabic_title": "حركة العلامة العشرية في الضرب والقسمة",
                "mastery": 0.50,
                "stability": 3.1,
                "last_practiced": "2026-09-30",
                "course_evidence": (
                    "عند الضرب في 10 أو 100 تتحرك العلامة جهة اليمين بعدد الأصفار (4.75 × 100 = 475). "
                    "عند القسمة على 10 تتحرك العلامة جهة اليسار (25.8 ÷ 10 = 2.58)."
                ),
                "sample_question": {
                    "question_id": "q_math_03",
                    "question_type": "mcq",
                    "lang": "ar",
                    "question_text": "ما هو ناتج ضرب: 4.75 × 100 ؟",
                    "hint": "تتحرك العلامة العشرية جهة اليمين خانتين بعدد أصفار الـ 100:",
                    "options": [
                        {"key": "A", "text": "475 (تحريك العلامة خانتين لليمين)", "is_correct": True},
                        {"key": "B", "text": "0.0475 (تحريك العلامة لليسار)", "is_correct": False, "misconception": "عكس اتجاه العلامة: تحريكها لليسار في الضرب"},
                        {"key": "C", "text": "47.5 (تحريك خانة واحدة فقط)", "is_correct": False, "misconception": "الضرب في 10 بدلاً من 100"},
                        {"key": "D", "text": "4750", "is_correct": False, "misconception": "زيادة خانة إضافية"}
                    ],
                    "accepted_text_answers": [
                        "475", "475.0", "أربعمائة وخمسة وسبعون", "A"
                    ],
                    "pedagogical_success_reply": "تسلم إيدك يا بطل! 🎯 عند الضرب في 100 حركت العلامة خانتين لليمين وأصبح الناتج 475، حل سليم 100%.",
                    "pedagogical_remediation_reply": "افتكر القاعدة السحرية يا شاطر: 🌟 في الضرب بنحرك العلامة ناحية اليمين (عشان الرقم يكبر)، وفي القسمة بنحركها ناحية الشمال. 4.75 × 100 = 475.",
                    "misconception_presets": [
                        {
                            "title": "مغالطة اتجاه حركة العلامة",
                            "answer": "0.0475 بتحريك العلامة لليسار",
                            "expected_misconception": "تحريك العلامة جهة اليسار في الضرب بدلاً من اليمين"
                        }
                    ]
                }
            },
            {
                "concept_id": "c_gcf_lcm",
                "concept_name": "العوامل والمضاعفات (ع.م.أ و م.م.أ)",
                "arabic_title": "العامل المشترك الأكبر والمضاعف المشترك الأصغر",
                "mastery": 0.38,
                "stability": 2.3,
                "last_practiced": "2026-09-27",
                "course_evidence": (
                    "للعددين 6 (2×3) و 8 (2×2×2): "
                    "العامل المشترك الأكبر (ع.م.أ) = 2 (العوامل المشتركة فقط). "
                    "المضاعف المشترك الأصغر (م.م.أ) = 2×3×2×2 = 24."
                ),
                "sample_question": {
                    "question_id": "q_math_04",
                    "question_type": "mcq",
                    "lang": "ar",
                    "question_text": "أوجد العامل المشترك الأكبر (ع.م.أ) والمضاعف المشترك الأصغر (م.م.أ) للعددين 6 و 8:",
                    "hint": "حلل العددين لعواملهما الأولية: 6 = 2×3 و 8 = 2×2×2:",
                    "options": [
                        {"key": "A", "text": "ع.م.أ = 2  و  م.م.أ = 24", "is_correct": True},
                        {"key": "B", "text": "ع.م.أ = 24  و  م.م.أ = 2", "is_correct": False, "misconception": "الخلط بين مفهوم العامل والمضاعف"},
                        {"key": "C", "text": "ع.م.أ = 1  و  م.م.أ = 48", "is_correct": False, "misconception": "ضرب العددين وتجاهل العوامل المشتركة"}
                    ],
                    "accepted_text_answers": [
                        "ع.م.أ = 2 و م.م.أ = 24", "ع.م.أ = 2 و م.م.أ = 24", "2 و 24", "2 ، 24", "A"
                    ],
                    "pedagogical_success_reply": "ممتاز جداً يا باشمهندس صغير! 👏 ع.م.أ = 2 لأنه أكبر عدد يقسمهم معاً، وم.م.أ = 24 لأنه أصغر عدد يقبل القسمة عليهم.",
                    "pedagogical_remediation_reply": "خلي بالك يا بطل: 💡 العامل (ع.م.أ) بيكون صغير (بيقسم العددين)، بينما المضاعف (م.م.أ) بيكون كبير (يقبل القسمة عليهم). للعددين 6 و 8: ع.م.أ = 2، وم.م.أ = 24.",
                    "misconception_presets": [
                        {
                            "title": "مغالطة عكس العامل والمضاعف",
                            "answer": "ع.م.أ = 24 و م.م.أ = 2",
                            "expected_misconception": "عكس مفهوم العامل والمضاعف بسبب كلمة أكبر وأصغر"
                        }
                    ]
                }
            }
        ]
    }
]
