# 🧩 Multi-Agent Collaboration Space

هذا المجلد مخصص لإضافة واستضافة وكلاء الذكاء الاصطناعي الإضافيين في المنظومة (مثل: **Course-Aware RAG Agent** أو **Interactive Tutoring Chat Agent** أو غيرهم من أعضاء الفريق).

---

## 📌 كيفية إضافة Agent جديد:

1. أنشئ مجلداً فرعياً خاصاً بالوكيل الجديد هنا، مثال:
   ```
   Other_AI_Agents/
   └── Course_Aware_RAG_Agent/
       ├── src/
       ├── tests/
       ├── requirements.txt
       └── README.md
   ```

2. **التكامل مع `Cognitive_Twin_AI_Agent`:**
   - وكيل الـ RAG يقوم بجلب وتمرير `course_evidence` إلى `Cognitive_Twin_AI_Agent`.
   - يقوم `Cognitive_Twin_AI_Agent` بتحليل الفهم وتحديد المفهوم الخاطئ والخطوة التعليمية التالية (`NextAction`).
