# 🧠 SALI AI Agents Package (`ai_agents/`)

مجموعة وكلاء الذكاء الاصطناعي (AI Agents) المستقلة الخاصة بمحرك التوأم المعرفي والتكيف التربوي: **SALI (Learner Intelligence & Adaptation Engine)**.

هذه الحزمة مصممة لتكون **مستقلة تماماً (Standalone)** بدون أي ارتباط بـ Frontend أو واجهات مستخدم، وجاهزة للاستيراد المباشر في أي كود Python، أو سيرفر FastAPI، أو Pipeline معالجة بيانات.

---

## 📂 هيكل المجلد (`ai_agents/`)

```
ai_agents/
├── __init__.py                     # نقطة الاستيراد وتصدير كافة الوكلاء
├── cognitive_twin_agent.py         # Agent 1: التوأم المعرفي ونموذج النسيان (BKT + Ebbinghaus)
├── misconception_agent.py          # Agent 2: كاشف المفاهيم الخاطئة والربط بالحالة المعرفية
├── adaptive_assessment_agent.py    # Agent 3: مولد الأسئلة التكيفية وصائد المفاهيم (ZPD)
├── next_action_agent.py            # Agent 4: صانع القرار البيداغوجي وتوجيه المعلم
├── closed_loop_agent.py            # Agent 5: منسق الدورة التعليمية الكاملة وإرسال الـ Webhooks
└── README.md                       # دليل الاستخدام والتوثيق
```

---

## 🚀 ملخص الوكلاء وطريقة استدعائهم:

### 1. `CognitiveTwinAgent` (Agent 1)
* **الوظيفة:** إدارة وتحديث احتمالية التمكن المعرفي باستخدام **Bayesian Knowledge Tracing (BKT)** وحساب التراجع في الذاكرة بمعادلة **Ebbinghaus Forgetting Curve** ($R = e^{-t/S}$).
* **الاستخدام:**
```python
from ai_agents import CognitiveTwinAgent, ConceptState, InteractionTelemetry

# الحالة الحالية للمفهوم
state = ConceptState(concept_id="c_python_ptr", concept_name="Pointers & Memory")

# تسجيل تفاعل جديد (إجابة صحيحة أو خاطئة)
telemetry = InteractionTelemetry(
    learner_id="learner_001",
    concept_id="c_python_ptr",
    concept_name="Pointers & Memory",
    is_correct=False,
    attempt_number=1
)

# تحديث التوأم المعرفي
updated_state = CognitiveTwinAgent.step(state, telemetry)
print(f"Mastery: {updated_state.p_known}, Forgetting Risk: {updated_state.forgetting_risk}")
```

---

### 2. `MisconceptionDetectionAgent` (Agent 2)
* **الوظيفة:** تجميع سجل أخطاء الطالب عبر المحاولات، تصنيف سبب الخطأ وفق تصنيف بيداغوجي صارم (`mental_model_flaw`, `negative_transfer`, `overgeneralization`, `slip`)، وخفض التمكن إذا تم تأكيد سوء الفهم.
* **الاستخدام:**
```python
from ai_agents import MisconceptionDetectionAgent, AttemptRecord

signal = MisconceptionDetectionAgent.diagnose(
    concept_name="Pointers & Memory",
    attempts=[
        AttemptRecord(attempt_number=1, question_id="q1", question_text="...", correct_answer="Ref", learner_answer="Copy", is_correct=False)
    ],
    current_question="What does assigning a list do?",
    correct_answer="Assigns reference",
    learner_answer="Makes a copy",
    is_correct=False,
    course_evidence="In Python, variable assignment binds a name to an object reference..."
)

print(f"Detected: {signal.detected} | Confidence: {signal.confidence_score} | Category: {signal.category}")
```

---

### 3. `AdaptiveAssessmentAgent` (Agent 3)
* **الوظيفة:** معايرة صعوبة السؤال ومستوى تصنيف بلوم (Bloom's Taxonomy) وفق منطقة النمو التقريبي (Zone of Proximal Development - ZPD) بالاعتماد على $P(L)$، وهندسة خيارات مضللة ذكية تستهدف صيد المفاهيم الخاطئة.
* **الاستخدام:**
```python
from ai_agents import AdaptiveAssessmentAgent

item = AdaptiveAssessmentAgent.generate_question(
    concept_name="Pointers & Memory",
    p_known=0.45,  # مستوى تمكن متوسط -> ينتج سؤال Apply / Intermediate
    rag_evidence="Python uses pass-by-assignment...",
    known_misconception="Treating references as deep copies"
)

print(f"Question: {item.question_text}")
print(f"Difficulty: {item.difficulty.value} | Bloom Tier: {item.bloom_level.value}")
```

---

### 4. `NextBestActionAgent` (Agent 4)
* **الوظيفة:** تنفيذ شجرة القواعد البيداغوجية لتحديد التدخل التعليمي القادم:
  * `escalation`: محاولات فاشلة $\ge 3$ أو إحباط $\rightarrow$ تنبيه وإعداد ملف تقرير للمعلم البشري.
  * `remediation`: مفهوم خاطئ مؤكد $\rightarrow$ شرح مقارن مستند لمنهج الكورس.
  * `socratic_tutoring`: خطأ عابر $\rightarrow$ سؤال توجيهي سقراطي بدون حرق الإجابة.
  * `practice`: إجابة صحيحة $\rightarrow$ تثبيت وتحدٍ جديد.
* **الاستخدام:**
```python
from ai_agents import NextBestActionAgent

plan = NextBestActionAgent.prescribe(
    learner_id="learner_001",
    concept_name="Pointers & Memory",
    consecutive_failures=3,
    attempt_number=3,
    frustration_flag=True,
    is_correct=False,
    p_known=0.20,
    course_evidence="Course excerpt..."
)

print(f"Prescribed Action: {plan.action_type.value}")
print(f"Message: {plan.response_content}")
```

---

### 5. `ClosedLoopOrchestratorAgent` (Agent 5)
* **الوظيفة:** إدارة وتشغيل الدورة التعليمية التكيفية الكاملة بخط أنابيب واحد يربط الوكلاء من 1 إلى 4، مع دعم استدعاء Webhook فوري عند حدوث تصعيد (Escalation).
* **الاستخدام المباشر:**
```python
from ai_agents import ClosedLoopOrchestratorAgent, ConceptState

def handle_webhook(data):
    print("Sending webhook to Slack / LMS:", data)

state = ConceptState(concept_id="c1", concept_name="Pointers & Memory")

result = ClosedLoopOrchestratorAgent.run_cycle(
    learner_id="alex_01",
    concept_id="c1",
    concept_name="Pointers & Memory",
    current_state=state,
    attempts=[],
    current_question="How are mutable objects passed?",
    correct_answer="By object reference",
    learner_answer="By value copy",
    is_correct=False,
    course_evidence="Variables hold references to objects in heap memory.",
    attempt_number=1,
    async_webhook_callback=handle_webhook
)

print(f"Updated Mastery: {result.updated_cognitive_state.p_known}")
print(f"Action: {result.prescribed_action.action_type.value}")
```
