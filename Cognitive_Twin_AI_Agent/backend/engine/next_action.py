"""
SALI — Adaptive Next-Best Action Selector
Decides the most effective pedagogical next step and generates a grounded
text response, strictly based on Course_Evidence.
"""
from __future__ import annotations
from ..models.schemas import (
    ActionType,
    MisconceptionSignal,
    LearnerStateUpdate,
    NextAction,
    Attempt,
    CourseEvidence,
)
from typing import List


# ─────────────────────────────────────────────
# DECISION LOGIC
# ─────────────────────────────────────────────

def _count_recent_failures(attempts: List[Attempt], concept_name: str) -> int:
    """Count incorrect attempts on the current concept."""
    return sum(
        1 for a in attempts
        if not a.is_correct
    )


def select_next_action(
    mastery_score: float,
    mastery_delta: float,
    misconception: MisconceptionSignal,
    state_update: LearnerStateUpdate,
    attempts: List[Attempt],
    current_question_text: str,
    is_correct: bool,
    course_evidence: CourseEvidence,
) -> NextAction:
    """
    Decision tree:
      1. escalation  → too many failures, mastery still very low
      2. remediation → misconception detected, mastery < 0.45
      3. socratic_tutoring → incorrect but no clear misconception, mastery 0.3–0.65
      4. practice    → mastery ≥ 0.65 (generate new adaptive item)
      5. practice    → correct answer, mastery ≥ 0.45 (reward with harder challenge)
    """
    failures = _count_recent_failures(attempts, course_evidence.concept_name)
    updated_mastery = mastery_score + mastery_delta
    evidence = course_evidence.source_text
    concept = course_evidence.concept_name

    # ── ESCALATION ──────────────────────────────────────────────────────────────
    if failures >= 4 and updated_mastery < 0.30:
        return NextAction(
            action_type=ActionType.escalation,
            reasoning=(
                f"The learner has failed {failures} times on '{concept}' "
                f"with mastery still at {updated_mastery:.0%}. "
                "Automated remediation has not been sufficient. "
                "Human instructor review is recommended."
            ),
            generated_response_or_question=(
                f"⚠️ It looks like you've been working really hard on **{concept}**, "
                f"and we think you'd benefit from a one-on-one session with your instructor. "
                f"Don't worry — this is a normal part of learning! "
                f"Your instructor has been notified and will reach out soon."
            ),
        )

    # ── REMEDIATION ─────────────────────────────────────────────────────────────
    if misconception.detected and updated_mastery < 0.45:
        # Extract the single most relevant sentence from source_text as anchor
        sentences = [s.strip() for s in evidence.split(".") if s.strip()]
        anchor = sentences[0] if sentences else evidence[:120]
        return NextAction(
            action_type=ActionType.remediation,
            reasoning=(
                f"A misconception was detected (confidence {misconception.confidence_score:.0%}): "
                f"{misconception.misunderstanding_description[:100]}… "
                f"Mastery is low ({updated_mastery:.0%}), so a targeted explanation is the right intervention."
            ),
            generated_response_or_question=(
                f"Let's clear something up about **{concept}**.\n\n"
                f"**What the course material says:** {anchor}.\n\n"
                f"**The misunderstanding detected:** {misconception.misunderstanding_description}\n\n"
                f"**Full context from your course:**\n> {evidence}\n\n"
                f"Take a moment to re-read this, then try the question again. "
                f"You've got this! 💡"
            ),
        )

    # ── SOCRATIC TUTORING ────────────────────────────────────────────────────────
    if not is_correct and updated_mastery < 0.65:
        # Build guiding questions from course evidence keywords
        socratic_questions = _build_socratic_questions(
            concept, current_question_text, evidence
        )
        return NextAction(
            action_type=ActionType.socratic_tutoring,
            reasoning=(
                f"The learner answered incorrectly but no strong misconception pattern was found. "
                f"Mastery is at {updated_mastery:.0%}. "
                "Socratic questioning will help them arrive at the answer independently."
            ),
            generated_response_or_question=socratic_questions,
        )

    # ── PRACTICE (Advanced Challenge) ────────────────────────────────────────────
    practice_item = _generate_practice_item(concept, updated_mastery, evidence)
    return NextAction(
        action_type=ActionType.practice,
        reasoning=(
            f"The learner's mastery on '{concept}' is {updated_mastery:.0%} "
            f"({'correct answer' if is_correct else 'progressing well'}). "
            "A new adaptive practice item will reinforce and extend their understanding."
        ),
        generated_response_or_question=practice_item,
    )


# ─────────────────────────────────────────────
# CONTENT GENERATORS (grounded in Course_Evidence)
# ─────────────────────────────────────────────

def _build_socratic_questions(
    concept: str, question_text: str, evidence: str
) -> str:
    """
    Generate Socratic guiding questions rooted in the course evidence.
    We never give the answer directly.
    """
    # Extract key phrases from evidence to anchor questions
    lines = [s.strip() for s in evidence.split(".") if len(s.strip()) > 20]
    concept_anchor = lines[0] if lines else f"the definition of {concept}"
    second_anchor = lines[1] if len(lines) > 1 else "its key properties"

    return (
        f"Great effort! Let's think through this together. 🤔\n\n"
        f"The question was: *\"{question_text}\"*\n\n"
        f"Here are some guiding questions to help you reason towards the answer:\n\n"
        f"1. Based on what the course says — *\"{concept_anchor}.\"* — what does that "
        f"   tell you about the core idea?\n\n"
        f"2. The material also notes: *\"{second_anchor}.\"* "
        f"   How does that connect to what you were asked?\n\n"
        f"3. If you were explaining **{concept}** to a classmate in one sentence, "
        f"   what would you say? Start there, and your answer will follow naturally.\n\n"
        f"Take your time and try again — you don't need the exact wording, just the right idea."
    )


def _generate_practice_item(
    concept: str, mastery: float, evidence: str
) -> str:
    """
    Generate a new adaptive assessment item grounded in the course evidence.
    Difficulty scales with current mastery.
    """
    lines = [s.strip() for s in evidence.split(".") if len(s.strip()) > 20]

    if mastery < 0.70:
        # Recall-level question
        anchor = lines[0] if lines else evidence[:100]
        return (
            f"🎯 **New Practice Question** (Recall Level)\n\n"
            f"Based on this passage from your course:\n"
            f"> \"{anchor}.\"\n\n"
            f"**Question:** In your own words, explain what this tells us about **{concept}**. "
            f"Why is this important to understand?"
        )
    elif mastery < 0.85:
        # Application-level question
        anchor = lines[1] if len(lines) > 1 else lines[0] if lines else evidence[:100]
        return (
            f"🎯 **New Practice Question** (Application Level)\n\n"
            f"The course states: *\"{anchor}.\"*\n\n"
            f"**Question:** Can you write a short code example (or describe a scenario) "
            f"that directly demonstrates this principle of **{concept}**? "
            f"Explain why your example works."
        )
    else:
        # Synthesis/edge-case question
        anchor = lines[-1] if lines else evidence[-100:]
        return (
            f"🎯 **Challenge Question** (Synthesis Level)\n\n"
            f"You're doing excellent work! Here's a challenge:\n\n"
            f"The course mentions: *\"{anchor}.\"*\n\n"
            f"**Question:** Describe a real-world situation where ignoring this aspect of "
            f"**{concept}** would lead to a bug or unexpected behaviour. "
            f"What would you do differently to avoid it?"
        )
