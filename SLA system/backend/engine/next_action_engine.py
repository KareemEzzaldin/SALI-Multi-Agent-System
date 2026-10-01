"""
SALI — Next-Best Action Engine (Step 4)
Orchestrates pedagogical decision tree rules (Escalation / Remediation / Socratic / Practice)
and generates Claude 3.5 Sonnet XML prompts for each adaptive intervention.
"""
from __future__ import annotations
from typing import Dict, Tuple, Optional
from ..models.schemas import ActionType, MisconceptionSignal
from ..models.next_action_models import (
    DecisionTelemetry,
    NextActionEvaluation,
    HumanEscalationDossier,
    NextActionDecisionRequest
)


class NextActionEngine:
    @staticmethod
    def evaluate_decision_rules(
        telemetry: DecisionTelemetry,
        is_correct: bool,
        p_known: float,
        misconception: Optional[MisconceptionSignal]
    ) -> Tuple[ActionType, str]:
        """
        Deterministic pedagogical decision hierarchy:
        1. Escalation: 3+ consecutive failures OR high frustration.
        2. Remediation: Confirmed misconception with confidence >= 0.50.
        3. Socratic Tutoring: Incorrect answer without deep structural misconception.
        4. Practice: Correct answer (spaced repetition / consolidation).
        """
        # 1. ESCALATION RULE
        if telemetry.consecutive_failures >= 3 or telemetry.frustration_detected or telemetry.attempt_number >= 4 and not is_correct:
            reason = (
                f"Learner has experienced {telemetry.consecutive_failures} consecutive failures "
                f"or acute cognitive friction on '{telemetry.concept_name}'. Automated nudges are "
                "yielding diminishing returns; human instructor intervention is required."
            )
            return ActionType.escalation, reason

        # 2. REMEDIATION RULE
        if not is_correct and misconception and misconception.detected and misconception.confidence_score >= 0.50:
            reason = (
                f"A distinct misconception was detected with {misconception.confidence_score:.0%} confidence: "
                f"'{misconception.misunderstanding_description[:100]}...'. Direct grounded remediation is indicated."
            )
            return ActionType.remediation, reason

        # 3. SOCRATIC TUTORING RULE
        if not is_correct:
            reason = (
                f"Learner made an incorrect attempt without an entrenched misconception. "
                f"Current mastery is {p_known:.0%}. Socratic scaffolding will encourage self-correction."
            )
            return ActionType.socratic_tutoring, reason

        # 4. PRACTICE RULE
        reason = (
            f"Learner answered correctly. Current mastery is {p_known:.0%}. "
            "Reinforcing retention through spaced repetition or adaptive advancement."
        )
        return ActionType.practice, reason

    @staticmethod
    def build_claude_tutor_prompt(
        action_type: ActionType,
        concept_name: str,
        question_text: str,
        learner_answer: str,
        course_evidence: str,
        misconception: Optional[MisconceptionSignal]
    ) -> Dict[str, str]:
        """
        Builds the Claude 3.5 Sonnet prompt with XML structuring tailored to the selected action.
        """
        if action_type == ActionType.socratic_tutoring:
            system_prompt = (
                "You are an expert Socratic Tutor for SALI (Secure Adaptive Learning Intelligence).\n"
                "Pedagogical Constraints:\n"
                "1. NEVER provide the direct answer or write corrected code.\n"
                "2. Ask exactly ONE focused, thought-provoking guiding question.\n"
                "3. Acknowledge what was partially correct or sensible in the student's thought process.\n"
                "4. Keep your response under 3 sentences."
            )
            user_prompt = f"""<pedagogical_mode>SOCRATIC_TUTORING</pedagogical_mode>
<context>
  <concept>{concept_name}</concept>
  <question>{question_text}</question>
  <student_answer>{learner_answer}</student_answer>
  <course_ground_truth>{course_evidence}</course_ground_truth>
</context>
<instruction>Generate a Socratic guiding response to help the student realize their misconception without giving the solution.</instruction>"""

        elif action_type == ActionType.remediation:
            system_prompt = (
                "You are the Remediation Specialist for SALI.\n"
                "Pedagogical Constraints:\n"
                "1. Directly address the identified misconception by contrasting what the student thought with the course ground truth.\n"
                "2. Ground your explanation strictly in the provided course evidence.\n"
                "3. Conclude with an encouraging invitation to re-attempt."
            )
            user_prompt = f"""<pedagogical_mode>GROUNDED_REMEDIATION</pedagogical_mode>
<context>
  <concept>{concept_name}</concept>
  <diagnosed_misconception>{misconception.misunderstanding_description if misconception else 'Conceptual confusion'}</diagnosed_misconception>
  <course_ground_truth>{course_evidence}</course_ground_truth>
</context>
<instruction>Generate a clear, respectful contrast between the misconception and the correct mechanical reality.</instruction>"""

        elif action_type == ActionType.escalation:
            system_prompt = (
                "You are the Pedagogical Handoff Coordinator for SALI.\n"
                "Your objective is twofold:\n"
                "1. Deliver an empathetic, reassuring message to the student explaining that a teacher has been notified.\n"
                "2. Generate a concise 3-bullet dossier for the human instructor outlining the conceptual roadblock."
            )
            user_prompt = f"""<pedagogical_mode>HUMAN_ESCALATION</pedagogical_mode>
<context>
  <concept>{concept_name}</concept>
  <failed_question>{question_text}</failed_question>
  <last_student_answer>{learner_answer}</last_student_answer>
</context>
<instruction>Generate the reassuring student message and the instructor diagnostic brief.</instruction>"""

        else:  # PRACTICE
            system_prompt = (
                "You are the Adaptive Learning Coach for SALI.\n"
                "Reinforce the student's success and summarize the key takeaway from the question."
            )
            user_prompt = f"""<pedagogical_mode>PRACTICE_CONSOLIDATION</pedagogical_mode>
<context>
  <concept>{concept_name}</concept>
  <course_evidence>{course_evidence}</course_evidence>
</context>
<instruction>Praise the student's correct reasoning and provide one memorable conceptual tip.</instruction>"""

        return {"system": system_prompt, "user": user_prompt}

    @classmethod
    def execute_decision_pipeline(
        cls,
        req: NextActionDecisionRequest,
        p_known: float
    ) -> NextActionEvaluation:
        """
        Executes rule evaluation, builds prompt, and generates grounded content.
        """
        action, reasoning = cls.evaluate_decision_rules(
            telemetry=req.telemetry,
            is_correct=req.is_correct,
            p_known=p_known,
            misconception=req.misconception_signal
        )

        human_dossier = None
        if action == ActionType.escalation:
            content = (
                f"You've put in great effort on **{req.telemetry.concept_name}**! "
                "We noticed this problem is proving tricky, so we have flagged this for your mentor. "
                "Take a 5-minute break while we queue up a targeted 1-on-1 walkthrough."
            )
            follow_up = "Notify assigned human instructor and pause automated penalties."
            human_dossier = HumanEscalationDossier(
                learner_id=req.telemetry.learner_id,
                concept_name=req.telemetry.concept_name,
                consecutive_failures=req.telemetry.consecutive_failures,
                diagnosed_block=f"Persistent failure on '{req.telemetry.concept_name}' after {req.telemetry.attempt_number} attempts.",
                suggested_human_intervention="Review foundational memory references and walk through diagrammatic state changes.",
                session_urgency="high" if req.telemetry.consecutive_failures >= 4 else "medium"
            )

        elif action == ActionType.remediation:
            snippet = req.course_evidence_text[:140]
            misc_desc = req.misconception_signal.misunderstanding_description if req.misconception_signal else "Conceptual misunderstanding"
            content = (
                f"Let's untangle this together. Notice how '{snippet}...' contradicts your current assumption. "
                f"Specifically: {misc_desc}. "
                "Review the excerpt above and try formulating the solution again!"
            )
            follow_up = "Deliver targeted practice question with distractor trap on next iteration."

        elif action == ActionType.socratic_tutoring:
            content = (
                f"You're very close! Think about what happens step-by-step when `{req.telemetry.concept_name}` evaluates: "
                "Does the value get copied into a separate location, or does the variable point directly to the existing object?"
            )
            follow_up = "Await student response to Socratic cue before altering difficulty."

        else:  # PRACTICE
            content = (
                f"Spot on! Your solution for **{req.telemetry.concept_name}** demonstrates solid understanding. "
                "Keep this momentum going—ready for the next challenge?"
            )
            follow_up = "Schedule next review in accordance with Ebbinghaus memory stability curve."

        return NextActionEvaluation(
            action_type=action,
            reasoning=reasoning,
            generated_content=content,
            follow_up_recommendation=follow_up,
            human_dossier=human_dossier
        )
