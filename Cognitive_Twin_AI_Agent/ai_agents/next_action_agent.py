"""
AI AGENT 4: Next-Best Action Pedagogical Agent
Implements:
- Multi-criteria Pedagogical Decision Engine Rules
- Action Modes: Escalation, Remediation, Socratic Tutoring, Practice
- Human Instructor Escalation Dossier Generator
- Claude 3.5 Sonnet Specialized Mode Prompts
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, Optional, Tuple
from pydantic import BaseModel, Field
from .misconception_agent import MisconceptionSignal


# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────

class ActionType(str, Enum):
    SOCRATIC_TUTORING = "socratic_tutoring"
    REMEDIATION = "remediation"
    PRACTICE = "practice"
    ESCALATION = "escalation"


class HumanDossier(BaseModel):
    learner_id: str
    concept_name: str
    consecutive_failures: int
    diagnosed_block: str
    urgency: str = "medium"


class ActionPlan(BaseModel):
    action_type: ActionType
    reasoning: str
    response_content: str
    follow_up_recommendation: str
    human_dossier: Optional[HumanDossier] = None


# ─────────────────────────────────────────────
# AGENT CORE
# ─────────────────────────────────────────────

class NextBestActionAgent:
    """
    Agent responsible for deciding the optimal pedagogical intervention and generating tutor guidance.
    """

    @staticmethod
    def evaluate_rules(
        consecutive_failures: int,
        attempt_number: int,
        frustration_flag: bool,
        is_correct: bool,
        p_known: float,
        misconception: Optional[MisconceptionSignal]
    ) -> Tuple[ActionType, str]:
        """
        Decision Hierarchy:
        1. Escalation: >=3 consecutive fails or frustration flag.
        2. Remediation: Confirmed misconception with confidence >= 0.50.
        3. Socratic Tutoring: Incorrect answer without chronic block.
        4. Practice: Correct answer (consolidation).
        """
        if consecutive_failures >= 3 or frustration_flag or (attempt_number >= 4 and not is_correct):
            return ActionType.ESCALATION, "Learner is experiencing acute cognitive friction; human intervention needed."

        if not is_correct and misconception and misconception.detected and misconception.confidence_score >= 0.50:
            return ActionType.REMEDIATION, f"Detected misconception: {misconception.misunderstanding_description[:80]}..."

        if not is_correct:
            return ActionType.SOCRATIC_TUTORING, "Error is transient/near-miss; scaffolding self-correction via Socratic cue."

        return ActionType.PRACTICE, f"Mastery verified ({p_known:.0%}); reinforcing retention via spaced challenge."

    @classmethod
    def prescribe(
        cls,
        learner_id: str,
        concept_name: str,
        consecutive_failures: int,
        attempt_number: int,
        frustration_flag: bool,
        is_correct: bool,
        p_known: float,
        course_evidence: str,
        misconception: Optional[MisconceptionSignal] = None
    ) -> ActionPlan:
        """Determines the action and drafts the grounded message."""
        action, reasoning = cls.evaluate_rules(
            consecutive_failures, attempt_number, frustration_flag, is_correct, p_known, misconception
        )

        dossier = None
        if action == ActionType.ESCALATION:
            content = (
                f"You've shown great dedication on **{concept_name}**! "
                "We've flagged this topic for your course mentor so you can have a quick 1-on-1 walkthrough. "
                "Feel free to take a short breather while we arrange that!"
            )
            dossier = HumanDossier(
                learner_id=learner_id,
                concept_name=concept_name,
                consecutive_failures=consecutive_failures,
                diagnosed_block=f"Persistent failure after {attempt_number} attempts on '{concept_name}'.",
                urgency="high" if consecutive_failures >= 4 else "medium"
            )
            rec = "Queue mentor session and freeze automated penalties."

        elif action == ActionType.REMEDIATION:
            snippet = course_evidence[:130]
            content = (
                f"Let's untangle this concept! The course material states: '{snippet}...'. "
                f"Your recent answers suggest a misunderstanding where: {misconception.misunderstanding_description if misconception else ''}. "
                "Compare these two perspectives and give it another try!"
            )
            rec = "Present targeted question containing distractor trap next."

        elif action == ActionType.SOCRATIC_TUTORING:
            content = (
                f"You are right on the edge of the solution! Think about how '{concept_name}' handles memory: "
                "Is a new copy created, or are you modifying the existing reference?"
            )
            rec = "Await student response to Socratic cue."

        else:
            content = (
                f"Excellent work on **{concept_name}**! Your reasoning was accurate. "
                "Let's keep this momentum rolling into the next challenge!"
            )
            rec = "Schedule next review according to Ebbinghaus memory stability."

        return ActionPlan(
            action_type=action,
            reasoning=reasoning,
            response_content=content,
            follow_up_recommendation=rec,
            human_dossier=dossier
        )

    @staticmethod
    def get_claude_tutor_prompt(action: ActionType, concept: str, question: str, answer: str, evidence: str) -> Dict[str, str]:
        """Generates Claude 3.5 Sonnet XML prompt according to pedagogical mode."""
        if action == ActionType.SOCRATIC_TUTORING:
            sys = "You are an expert Socratic Tutor for SALI. NEVER reveal the answer. Ask ONE focused reflective question."
            mode = "SOCRATIC_TUTORING"
        elif action == ActionType.REMEDIATION:
            sys = "You are the Remediation Specialist for SALI. Contrast the student's assumption with course ground truth."
            mode = "GROUNDED_REMEDIATION"
        elif action == ActionType.ESCALATION:
            sys = "You are the Pedagogical Handoff Coordinator for SALI. Deliver an empathetic message to the student and brief the instructor."
            mode = "HUMAN_ESCALATION"
        else:
            sys = "You are the Adaptive Learning Coach for SALI. Praise correct reasoning and reinforce the core takeaway."
            mode = "PRACTICE_CONSOLIDATION"

        usr = f"""<pedagogical_mode>{mode}</pedagogical_mode>
<context>
  <concept>{concept}</concept>
  <question>{question}</question>
  <student_answer>{answer}</student_answer>
  <course_evidence>{evidence}</course_evidence>
</context>
<instruction>Generate response tailored to {mode}.</instruction>"""
        return {"system": sys, "user": usr}
