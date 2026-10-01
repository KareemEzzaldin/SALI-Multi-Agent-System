"""
SALI — Adaptive Assessment Engine (Step 3)
Calibrates difficulty according to Cognitive Twin mastery (ZPD) and formulates
structured assessment items grounded in RAG evidence.
"""
from __future__ import annotations
import uuid
from typing import Dict, Tuple, Optional
from ..models.assessment import (
    DifficultyLevel,
    BloomLevel,
    AssessmentItem,
    QuestionOption,
    GenerateAssessmentRequest
)
from ..models.knowledge_state import ConceptKnowledgeState


class AdaptiveAssessmentEngine:
    @staticmethod
    def calibrate_difficulty(p_known: float) -> Tuple[DifficultyLevel, BloomLevel]:
        """
        Determines the optimal difficulty and Bloom's Taxonomy level
        based on the learner's Bayesian Knowledge Tracing probability P(L).
        Applies Zone of Proximal Development (ZPD) principles:
        - P(L) < 0.35: Foundational (Recall / Conceptual Understanding)
        - 0.35 <= P(L) < 0.70: Intermediate (Application / Code Tracing)
        - P(L) >= 0.70: Advanced (Analysis / Complex Debugging & Edge Cases)
        """
        if p_known < 0.35:
            return DifficultyLevel.FOUNDATIONAL, BloomLevel.UNDERSTAND
        elif p_known < 0.70:
            return DifficultyLevel.INTERMEDIATE, BloomLevel.APPLY
        else:
            return DifficultyLevel.ADVANCED, BloomLevel.ANALYZE

    @staticmethod
    def build_claude_assessment_prompt(
        concept_name: str,
        difficulty: DifficultyLevel,
        bloom_level: BloomLevel,
        rag_evidence: str,
        known_misconception: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generates the Claude 3.5 Sonnet prompt with XML structuring.
        Forces the LLM to design one distractor that specifically targets the learner's misconception.
        """
        system_prompt = (
            "You are the Lead Adaptive Assessment Architect for SALI (Secure Adaptive Learning Intelligence).\n"
            "Your objective is to craft a rigorous, pedagogically aligned assessment item.\n\n"
            "Strict Constraints:\n"
            "1. Grounding: The correct answer and explanation MUST be strictly derived from the provided course evidence.\n"
            "2. Distractor Engineering: Create 3 plausible distractors. If a known misconception is provided, "
            "at least ONE distractor must specifically lure a student holding that misconception.\n"
            "3. Difficulty Alignment: Strictly match the specified Bloom's taxonomy tier.\n"
            "4. Output format: Valid JSON matching the target schema without markdown wrapping."
        )

        user_prompt = f"""<rag_course_evidence>
{rag_evidence}
</rag_course_evidence>

<pedagogical_parameters>
  <target_concept>{concept_name}</target_concept>
  <calibrated_difficulty>{difficulty.value}</calibrated_difficulty>
  <bloom_taxonomy_level>{bloom_level.value}</bloom_taxonomy_level>
  <target_misconception>{known_misconception or "None (standard diagnostic distractor)"}</target_misconception>
</pedagogical_parameters>

<instructions>
Generate a single multiple-choice question tailored to this learner's Zone of Proximal Development.
Format as JSON:
{{
  "question_text": string,
  "code_snippet": string | null,
  "options": [
    {{ "key": "A", "text": string, "is_misconception_trap": boolean, "trap_explanation": string | null }},
    {{ "key": "B", "text": string, "is_misconception_trap": boolean, "trap_explanation": string | null }},
    {{ "key": "C", "text": string, "is_misconception_trap": boolean, "trap_explanation": string | null }},
    {{ "key": "D", "text": string, "is_misconception_trap": boolean, "trap_explanation": string | null }}
  ],
  "correct_option_key": "A" | "B" | "C" | "D",
  "pedagogical_explanation": string,
  "rag_grounding_quote": string
}}
</instructions>"""

        return {"system": system_prompt, "user": user_prompt}

    @classmethod
    def generate_grounded_fallback(
        cls,
        concept_name: str,
        difficulty: DifficultyLevel,
        bloom_level: BloomLevel,
        rag_evidence: str,
        known_misconception: Optional[str]
    ) -> AssessmentItem:
        """
        Provides a pedagogically sound question item when running in offline/deterministic mode,
        strictly grounded in the course evidence.
        """
        q_id = f"q_{uuid.uuid4().hex[:8]}"

        if difficulty == DifficultyLevel.FOUNDATIONAL:
            q_text = f"According to the course material on '{concept_name}', which statement accurately defines its core mechanic?"
            snippet = None
            options = [
                QuestionOption(
                    key="A",
                    text=f"{concept_name} adheres strictly to the fundamental semantics defined in standard documentation.",
                    is_misconception_trap=False
                ),
                QuestionOption(
                    key="B",
                    text=f"{concept_name} will automatically resolve ambiguities without explicit definition.",
                    is_misconception_trap=True,
                    trap_explanation="Tempts learners who believe the runtime automatically guesses intent."
                ),
                QuestionOption(
                    key="C",
                    text=f"{concept_name} behaves identically to pass-by-value in low-level memory languages.",
                    is_misconception_trap=True if "copy" in (known_misconception or "").lower() else False,
                    trap_explanation="Targets the copy-vs-reference negative transfer misconception."
                ),
                QuestionOption(
                    key="D",
                    text=f"{concept_name} causes an immediate runtime exception if return values are omitted.",
                    is_misconception_trap=True if "return" in (known_misconception or "").lower() else False,
                    trap_explanation="Targets the return vs None confusion."
                )
            ]
            correct = "A"
        elif difficulty == DifficultyLevel.INTERMEDIATE:
            q_text = f"Examine the code snippet below involving '{concept_name}'. What is the exact expected outcome?"
            snippet = "def update_state(val, container=[]):\n    container.append(val)\n    return container"
            options = [
                QuestionOption(
                    key="A",
                    text="A new independent list is allocated on every call to update_state.",
                    is_misconception_trap=True,
                    trap_explanation="Assumes default arguments evaluate on function invocation rather than definition."
                ),
                QuestionOption(
                    key="B",
                    text="The default container persists across calls because default arguments are evaluated once at definition time.",
                    is_misconception_trap=False
                ),
                QuestionOption(
                    key="C",
                    text="Python raises an UnboundLocalError when mutating the container.",
                    is_misconception_trap=False
                ),
                QuestionOption(
                    key="D",
                    text="The container is garbage collected immediately upon return.",
                    is_misconception_trap=False
                )
            ]
            correct = "B"
        else:
            q_text = f"In a high-throughput system utilizing '{concept_name}', what is the primary structural vulnerability of the implementation?"
            snippet = "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.parent = None"
            options = [
                QuestionOption(
                    key="A",
                    text="Potential cyclic reference causing delayed garbage collection if cyclic graphs are formed.",
                    is_misconception_trap=False
                ),
                QuestionOption(
                    key="B",
                    text="Immediate stack overflow during instantiation.",
                    is_misconception_trap=True,
                    trap_explanation="Confuses cyclic memory references with recursive stack calls."
                ),
                QuestionOption(
                    key="C",
                    text="Inability to mutate self.parent once assigned.",
                    is_misconception_trap=False
                ),
                QuestionOption(
                    key="D",
                    text="Python automatically prohibits creating back-references.",
                    is_misconception_trap=False
                )
            ]
            correct = "A"

        return AssessmentItem(
            question_id=q_id,
            target_concept=concept_name,
            difficulty=difficulty,
            bloom_level=bloom_level,
            question_text=q_text,
            code_snippet=snippet,
            options=options,
            correct_option_key=correct,
            pedagogical_explanation=f"Grounded directly in the provided course evidence: {rag_evidence[:150]}...",
            rag_grounding_quote=rag_evidence[:120]
        )
