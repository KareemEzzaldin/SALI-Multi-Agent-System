# 🚀 SALI Multi-Agent Adaptive Learning System

مستودع شامل وموزع لاستضافة وكلاء الذكاء الاصطناعي (AI Agents) الخاصة بنظام التعلم التكيفي المغلق **SALI (Secure Adaptive Learning Intelligence)**.

---

## 🏗️ هيكل المستودع (Repository Structure)

```
├── Cognitive_Twin_AI_Agent/      # 🧠 نموذج التوأم المعرفي والتكيف التربوي (Cognitive Twin Engine)
│   ├── ai_agents/                # نماذج الذكاء الاصطناعي المستقلة الخمسة (Pure Python)
│   │   ├── cognitive_twin_agent.py
│   │   ├── misconception_agent.py
│   │   ├── adaptive_assessment_agent.py
│   │   ├── next_action_agent.py
│   │   └── closed_loop_agent.py
│   ├── backend/                  # خادم FastAPI ومسارات الـ REST API
│   ├── requirements.txt          # متطلبات التشغيل
│   └── README.md                 # توثيق خاص بالـ Cognitive Twin
│
├── Other_AI_Agents/              # 🧩 مساحة مخصصة لباقي أعضاء الفريق لإضافة الوكلاء الآخرين
│   └── README.md                 # دليل التنسيق وإضافة وكلاء جدد (مثل: Course-Aware RAG Agent)
│
├── .gitignore                    # استبعاد الملفات المؤقتة وبيئة العمل
└── README.md                     # التوثيق الرئيسي للنظام
```

---

## 🤖 نظرة على وكلاء المنظومة (Agents Overview)

| الوكيل | المسار | الوظيفة الأساسية |
| :--- | :--- | :--- |
| **Cognitive Twin Agent** | `Cognitive_Twin_AI_Agent/ai_agents/cognitive_twin_agent.py` | نمذجة المعرفة عبر BKT وحساب التراجع في الذاكرة بمعادلة إبنجهاوس للنسيان ($R = e^{-t/S}$) |
| **Misconception Agent** | `Cognitive_Twin_AI_Agent/ai_agents/misconception_agent.py` | كاشف الجذور المعرفية للأخطاء المتكررة وتصنيفها وربطها بالتمكن |
| **Adaptive Assessment** | `Cognitive_Twin_AI_Agent/ai_agents/adaptive_assessment_agent.py` | توليد أسئلة تكيفية في منطقة النمو التقريبي (ZPD) وهندسة مشتتات لاصطياد الفهم الخاطئ |
| **Next-Best Action** | `Cognitive_Twin_AI_Agent/ai_agents/next_action_agent.py` | شجرة قرارات تربوية (Escalation / Remediation / Socratic / Practice) |
| **Closed-Loop Orchestrator** | `Cognitive_Twin_AI_Agent/ai_agents/closed_loop_agent.py` | ربط الوكلاء بدورة مغلقة متكاملة وتشغيل تنبيهات الـ Webhooks للمعلم البشري |

---

## 💻 طريقة تشغيل الـ Cognitive Twin Agent

```bash
# 1. الدخول لمجلد الوكيل
cd Cognitive_Twin_AI_Agent

# 2. تثبيت المكتبات
pip install -r requirements.txt

# 3. تشغيل الـ FastAPI Engine
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
