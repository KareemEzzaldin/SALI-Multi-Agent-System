"""
SALI — Misconception Detection Engine (Step 2)
Integrates History Aggregation, Claude 3.5 Sonnet Diagnostic Pattern Analysis,
and State Linking with the Cognitive Twin.
"""
from __future__ import annotations
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..models.schemas import Attempt, MisconceptionSignal
from ..models.knowledge_state import ConceptKnowledgeState


# ─────────────────────────────────────────────
# HISTORY AGGREGATION
# ─────────────────────────────────────────────

class AggregatedAttemptHistory(BaseModel):
    """Structured summary of learner's historical friction on a concept."""
    concept_name: str
    total_attempts: int
    failed_attempts_count: int
    consecutive_failures: int
    distinct_wrong_answers: List[str]
    interaction_timeline: List[Dict[str, Any]]
    has_chronic_failure: bool


class MisconceptionDiagnosticResult(BaseModel):
    """Enriched diagnostic signal linked with pedagogical state."""
    signal: MisconceptionSignal
    category: str = Field(
        "none",
        description="Category: 'mental_model_flaw' | 'negative_transfer' | 'overgeneralization' | 'slip' | 'none'"
    )
    linked_state: Optional[ConceptKnowledgeState] = None


class HistoryAggregator:
    @staticmethod
    def aggregate(
        attempts: List[Attempt],
        concept_name: str,
        current_answer: str,
        is_correct: bool
    ) -> AggregatedAttemptHistory:
        """
        Aggregates past attempts, extracts recurring error patterns,
        and builds an empirical timeline for Claude 3.5 Sonnet analysis.
        """
        # Filter attempts relevant to the target concept (or all if concept is generic)
        wrong_answers: List[str] = []
        timeline: List[Dict[str, Any]] = []
        consecutive_fails = 0

        for a in attempts:
            if not a.is_correct:
                consecutive_fails += 1
                if a.learner_answer not in wrong_answers:
                    wrong_answers.append(a.learner_answer)
            else:
                consecutive_fails = 0

            timeline.append({
                "attempt_number": a.attempt_number,
                "question_id": a.question_id,
                "learner_answer": a.learner_answer,
                "correct_answer": a.correct_answer,
                "is_correct": a.is_correct,
                "timestamp": a.timestamp
            })

        # Append current interaction into evaluation
        if not is_correct:
            consecutive_fails += 1
            if current_answer not in wrong_answers:
                wrong_answers.append(current_answer)
        else:
            consecutive_fails = 0

        total = len(attempts) + 1
        failed_count = sum(1 for a in attempts if not a.is_correct) + (0 if is_correct else 1)

        return AggregatedAttemptHistory(
            concept_name=concept_name,
            total_attempts=total,
            failed_attempts_count=failed_count,
            consecutive_failures=consecutive_fails,
            distinct_wrong_answers=wrong_answers,
            interaction_timeline=timeline,
            has_chronic_failure=consecutive_fails >= 2
        )


# ─────────────────────────────────────────────
# CLAUDE 3.5 SONNET PROMPT GENERATOR
# ─────────────────────────────────────────────

def build_claude_misconception_prompt(
    aggregated_history: AggregatedAttemptHistory,
    question_text: str,
    correct_answer: str,
    learner_answer: str,
    course_evidence_snippet: str
) -> Dict[str, str]:
    """
    Constructs the exact system and user prompts optimized for Claude 3.5 Sonnet's
    XML-tagged cognitive diagnostic reasoning.
    """
    system_prompt = (
        "You are the Lead Misconception Diagnostic Agent for SALI (Secure Adaptive Learning Intelligence).\n"
        "Your mission is to perform root-cause cognitive analysis on a student's repeated errors.\n"
        "Do NOT simply state that the answer is incorrect. You must diagnose the underlying flawed mental model.\n\n"
        "Diagnostic Taxonomy:\n"
        "- 'mental_model_flaw': Flawed conceptual understanding of internal mechanics (e.g. pointer vs value, scope).\n"
        "- 'negative_transfer': Erroneous syntax or rules imported from other programming languages.\n"
        "- 'overgeneralization': Incorrectly applying a valid rule outside its intended domain.\n"
        "- 'slip': Accidental syntax error or typographical oversight without deep conceptual misunderstanding.\n\n"
        "Guidelines:\n"
        "1. Analyze the interaction trajectory inside <thinking> tags before concluding.\n"
        "2. Ground your findings strictly in the provided course evidence.\n"
        "3. If the answer is correct or a benign typo, set detected=false with confidence=0.0.\n"
        "4. Output strictly valid JSON matching the target schema without markdown wrap."
    )

    user_prompt = f"""<pedagogical_context>
  <target_concept>{aggregated_history.concept_name}</target_concept>
  <course_evidence>{course_evidence_snippet}</course_evidence>
</pedagogical_context>

<learner_history>
  <total_attempts>{aggregated_history.total_attempts}</total_attempts>
  <failed_attempts>{aggregated_history.failed_attempts_count}</failed_attempts>
  <consecutive_failures>{aggregated_history.consecutive_failures}</consecutive_failures>
  <distinct_wrong_answers>{json.dumps(aggregated_history.distinct_wrong_answers)}</distinct_wrong_answers>
</learner_history>

<current_interaction>
  <question>{question_text}</question>
  <correct_answer>{correct_answer}</correct_answer>
  <learner_answer>{learner_answer}</learner_answer>
</current_interaction>

<instructions>
Formulate a cognitive diagnosis. Respond with a JSON object strictly conforming to:
{{
  "detected": boolean,
  "concept_name": "{aggregated_history.concept_name}",
  "misunderstanding_description": string,
  "confidence_score": float (between 0.0 and 1.0),
  "category": "mental_model_flaw" | "negative_transfer" | "overgeneralization" | "slip" | "none"
}}
</instructions>"""

    return {"system": system_prompt, "user": user_prompt}


# ─────────────────────────────────────────────
# STATE LINKING ENGINE
# ─────────────────────────────────────────────

class MisconceptionStateLinker:
    @staticmethod
    def link_to_cognitive_twin(
        state: ConceptKnowledgeState,
        misconception: MisconceptionSignal,
        category: str
    ) -> ConceptKnowledgeState:
        """
        Links detected misconception back to the learner's Cognitive Twin:
        - If chronic mental_model_flaw is detected with high confidence (> 0.70),
          we depress BKT p_known to reflect ungrounded mastery.
        - Reduces memory stability S to trigger sooner review intervals.
        """
        if not misconception.detected or misconception.confidence_score < 0.50:
            return state

        penalty_factor = 0.85
        if category == "mental_model_flaw":
            penalty_factor = 0.75  # Deeper penalty for foundational misconceptions
        elif category == "negative_transfer":
            penalty_factor = 0.80

        # Adjust BKT mastery probability
        depressed_p_known = round(max(state.p_known * penalty_factor, 0.05), 4)

        # Halve memory stability to prioritize adaptive intervention
        new_stability = round(max(state.memory_stability * 0.70, 0.5), 2)

        return state.model_copy(update={
            "p_known": depressed_p_known,
            "memory_stability": new_stability,
            "consecutive_correct": 0
        })
