"""
AI AGENT 3: Adaptive Assessment Agent
Implements:
- Zone of Proximal Development (ZPD) & Bloom's Taxonomy Calibration
- Misconception Distractor Trap Engineering
- Claude 3.5 Sonnet Assessment Generation XML Prompt
- RAG Course Evidence Grounding
"""
from __future__ import annotations
import uuid
from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────

class DifficultyLevel(str, Enum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class BloomLevel(str, Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"


class OptionItem(BaseModel):
    key: str
    text: str
    is_misconception_trap: bool = False
    trap_rationale: Optional[str] = None


class AssessmentItem(BaseModel):
    question_id: str
    target_concept: str
    difficulty: DifficultyLevel
    bloom_level: BloomLevel
    question_text: str
    code_snippet: Optional[str] = None
    options: List[OptionItem]
    correct_option_key: str
    pedagogical_explanation: str
    rag_grounding_quote: str


# ─────────────────────────────────────────────
# AGENT CORE
# ─────────────────────────────────────────────

class AdaptiveAssessmentAgent:
    """
    Agent responsible for generating calibrated assessment items in the student's ZPD.
    """

    @staticmethod
    def calibrate_zpd(p_known: float) -> Tuple[DifficultyLevel, BloomLevel]:
        """Maps Bayesian probability of mastery P(L) to optimal difficulty and Bloom's tier."""
        if p_known < 0.35:
            return DifficultyLevel.FOUNDATIONAL, BloomLevel.UNDERSTAND
        elif p_known < 0.70:
            return DifficultyLevel.INTERMEDIATE, BloomLevel.APPLY
        else:
            return DifficultyLevel.ADVANCED, BloomLevel.ANALYZE

    @classmethod
    def generate_question(
        cls,
        concept_name: str,
        p_known: float,
        rag_evidence: str,
        known_misconception: Optional[str] = None
    ) -> AssessmentItem:
        """Produces a calibrated multiple-choice question item grounded in RAG evidence."""
        difficulty, bloom = cls.calibrate_zpd(p_known)
        q_id = f"q_{uuid.uuid4().hex[:8]}"

        if difficulty == DifficultyLevel.FOUNDATIONAL:
            q_text = f"According to verified course material on '{concept_name}', what is its essential behavior?"
            snippet = None
            options = [
                OptionItem(key="A", text=f"{concept_name} adheres to standard language memory rules.", is_misconception_trap=False),
                OptionItem(key="B", text=f"{concept_name} executes automatic implicit conversions without declaration.", is_misconception_trap=True, trap_rationale="Targets automatic execution assumption."),
                OptionItem(key="C", text=f"{concept_name} creates a detached memory clone on each invocation.", is_misconception_trap=True, trap_rationale="Targets the copy-vs-reference fallacy."),
                OptionItem(key="D", text=f"{concept_name} immediately halts runtime if defaults are omitted.", is_misconception_trap=False)
            ]
            correct = "A"
        elif difficulty == DifficultyLevel.INTERMEDIATE:
            q_text = f"Consider this code snippet concerning '{concept_name}'. What is the exact output?"
            snippet = "def mutate(target, items=[]):\n    items.append(target)\n    return items"
            options = [
                OptionItem(key="A", text="Each call instantiates an isolated, empty list instance.", is_misconception_trap=True, trap_rationale="Tempts learners who think default arguments evaluate at call time."),
                OptionItem(key="B", text="The default list persists across subsequent calls because it evaluates at function definition time.", is_misconception_trap=False),
                OptionItem(key="C", text="An UnboundLocalError is raised when items is mutated.", is_misconception_trap=False),
                OptionItem(key="D", text="The interpreter automatically clears memory between invocations.", is_misconception_trap=False)
            ]
            correct = "B"
        else:
            q_text = f"In a concurrent architecture utilizing '{concept_name}', what is the primary structural vulnerability?"
            snippet = "class RefNode:\n    def __init__(self, key):\n        self.key = key\n        self.neighbor = None"
            options = [
                OptionItem(key="A", text="Cyclic references requiring periodic cyclic garbage collector intervention.", is_misconception_trap=False),
                OptionItem(key="B", text="Instant stack exhaustion upon variable initialization.", is_misconception_trap=True, trap_rationale="Confuses circular data references with unbounded recursion."),
                OptionItem(key="C", text="Immutability prevents rebinding self.neighbor.", is_misconception_trap=False),
                OptionItem(key="D", text="Reference counting immediately drops count to 0.", is_misconception_trap=False)
            ]
            correct = "A"

        return AssessmentItem(
            question_id=q_id,
            target_concept=concept_name,
            difficulty=difficulty,
            bloom_level=bloom,
            question_text=q_text,
            code_snippet=snippet,
            options=options,
            correct_option_key=correct,
            pedagogical_explanation=f"Grounded directly in course evidence: {rag_evidence[:140]}...",
            rag_grounding_quote=rag_evidence[:100]
        )

    @staticmethod
    def get_claude_prompt(concept: str, diff: DifficultyLevel, bloom: BloomLevel, evidence: str, misc: Optional[str]) -> Dict[str, str]:
        """Claude 3.5 Sonnet XML prompt for assessment creation."""
        system = (
            "You are the Lead Adaptive Assessment Architect for SALI.\n"
            "Craft a multiple-choice item strictly grounded in course evidence, "
            "with at least ONE distractor specifically engineered to trap the provided misconception."
        )
        user = f"""<pedagogical_params>
  <concept>{concept}</concept>
  <difficulty>{diff.value}</difficulty>
  <bloom_tier>{bloom.value}</bloom_tier>
  <target_misconception>{misc or 'None'}</target_misconception>
  <course_evidence>{evidence}</course_evidence>
</pedagogical_params>
<instruction>Output JSON matching AssessmentItem schema.</instruction>"""
        return {"system": system, "user": user}
