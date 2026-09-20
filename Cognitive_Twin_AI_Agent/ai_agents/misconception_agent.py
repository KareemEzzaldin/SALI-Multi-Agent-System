"""
AI AGENT 2: Misconception Detection Agent
Implements:
- Attempt History Aggregator across interactions
- Cognitive Root-Cause Diagnostic Taxonomy
- Claude 3.5 Sonnet XML Diagnostic Prompt
- State Linking with Cognitive Twin
"""
from __future__ import annotations
import json
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from .cognitive_twin_agent import ConceptState


# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────

class AttemptRecord(BaseModel):
    attempt_number: int
    question_id: str
    question_text: str
    correct_answer: str
    learner_answer: str
    is_correct: bool


class MisconceptionSignal(BaseModel):
    detected: bool
    concept_name: str
    misunderstanding_description: str
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)
    category: str = Field("none", description="'mental_model_flaw' | 'negative_transfer' | 'overgeneralization' | 'slip' | 'none'")


# ─────────────────────────────────────────────
# AGENT CORE
# ─────────────────────────────────────────────

class MisconceptionDetectionAgent:
    """
    Agent responsible for diagnosing the root mental model flaw behind recurring errors.
    """

    @staticmethod
    def aggregate_history(attempts: List[AttemptRecord], current_answer: str, is_correct: bool) -> Dict[str, Any]:
        """Extracts failure count, consecutive failures, and distinct wrong answers."""
        wrong_answers = []
        consecutive_fails = 0

        for a in attempts:
            if not a.is_correct:
                consecutive_fails += 1
                if a.learner_answer not in wrong_answers:
                    wrong_answers.append(a.learner_answer)
            else:
                consecutive_fails = 0

        if not is_correct:
            consecutive_fails += 1
            if current_answer not in wrong_answers:
                wrong_answers.append(current_answer)
        else:
            consecutive_fails = 0

        failed_count = sum(1 for a in attempts if not a.is_correct) + (0 if is_correct else 1)

        return {
            "total_attempts": len(attempts) + 1,
            "failed_attempts": failed_count,
            "consecutive_failures": consecutive_fails,
            "distinct_wrong_answers": wrong_answers,
            "is_chronic": consecutive_fails >= 2
        }

    @classmethod
    def diagnose(
        cls,
        concept_name: str,
        attempts: List[AttemptRecord],
        current_question: str,
        correct_answer: str,
        learner_answer: str,
        is_correct: bool,
        course_evidence: str
    ) -> MisconceptionSignal:
        """Evaluates history and produces the structured MisconceptionSignal."""
        summary = cls.aggregate_history(attempts, learner_answer, is_correct)

        if not is_correct and summary["failed_attempts"] >= 1:
            detected = True
            confidence = min(0.60 + 0.15 * summary["consecutive_failures"], 0.95)
            category = "mental_model_flaw"
            desc = (
                f"Persistent confusion detected in '{concept_name}'. Learner repeatedly misapplies "
                f"core mechanics across {summary['failed_attempts']} failed attempts."
            )
        else:
            detected = False
            confidence = 0.0
            category = "none"
            desc = "No recurring misconception detected. Error appears transient or answer is correct."

        return MisconceptionSignal(
            detected=detected,
            concept_name=concept_name,
            misunderstanding_description=desc,
            confidence_score=round(confidence, 2),
            category=category
        )

    @staticmethod
    def link_state(state: ConceptState, signal: MisconceptionSignal) -> ConceptState:
        """Depresses mastery and memory stability if a foundational misconception is confirmed."""
        if not signal.detected or signal.confidence_score < 0.50:
            return state

        penalty = 0.75 if signal.category == "mental_model_flaw" else 0.85
        new_p_known = round(max(state.p_known * penalty, 0.05), 4)
        new_stability = round(max(state.memory_stability * 0.70, 0.5), 2)

        return state.model_copy(update={
            "p_known": new_p_known,
            "memory_stability": new_stability,
            "consecutive_correct": 0
        })

    @staticmethod
    def get_claude_prompt(
        concept_name: str,
        history_summary: Dict[str, Any],
        question: str,
        correct: str,
        answer: str,
        course_evidence: str
    ) -> Dict[str, str]:
        """Generates Claude 3.5 Sonnet XML diagnostic prompt."""
        system = (
            "You are the Lead Misconception Diagnostic Agent for SALI.\n"
            "Diagnose the underlying flawed mental model from the student's repeated error patterns.\n"
            "Taxonomy: 'mental_model_flaw' | 'negative_transfer' | 'overgeneralization' | 'slip' | 'none'"
        )
        user = f"""<pedagogical_context>
  <concept>{concept_name}</concept>
  <course_evidence>{course_evidence}</course_evidence>
</pedagogical_context>
<learner_history>
  <total_attempts>{history_summary['total_attempts']}</total_attempts>
  <consecutive_failures>{history_summary['consecutive_failures']}</consecutive_failures>
  <distinct_wrong_answers>{json.dumps(history_summary['distinct_wrong_answers'])}</distinct_wrong_answers>
</learner_history>
<current_interaction>
  <question>{question}</question>
  <correct_answer>{correct}</correct_answer>
  <learner_answer>{answer}</learner_answer>
</current_interaction>
<instruction>Output JSON matching MisconceptionSignal schema.</instruction>"""
        return {"system": system, "user": user}
