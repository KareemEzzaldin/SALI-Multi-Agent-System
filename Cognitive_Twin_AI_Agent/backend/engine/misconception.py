"""
SALI — Misconception Detection Engine
Analyses attempt history to identify recurring error patterns and formulate
a hypothesis about the learner's underlying misunderstanding.
"""
from __future__ import annotations
from typing import List
from ..models.schemas import Attempt, MisconceptionSignal


# ─────────────────────────────────────────────
# KNOWN ERROR PATTERN CATALOGUE
# Maps (concept_name, keyword_in_wrong_answer) → misunderstanding hypothesis
# ─────────────────────────────────────────────
_ERROR_PATTERNS: list[dict] = [
    {
        "concept": "Python Functions",
        "wrong_keywords": ["error", "nothing", "crash", "exception"],
        "misunderstanding": (
            "The learner believes that a function without a `return` statement produces an error "
            "or does nothing. They have not yet internalised that Python implicitly returns `None` "
            "from any function that lacks an explicit return."
        ),
        "trigger_question_ids": ["q_func_001"],
    },
    {
        "concept": "Python Functions",
        "wrong_keywords": ["0", "zero", "empty", "null"],
        "misunderstanding": (
            "The learner conflates Python's `None` with numeric zero or an empty value. "
            "This is a type-confusion misconception: `None` is a singleton object of type `NoneType`, "
            "not a numeric or empty-string default."
        ),
        "trigger_question_ids": ["q_func_001"],
    },
    {
        "concept": "Python Functions",
        "wrong_keywords": ["same", "identical", "equivalent", "both"],
        "misunderstanding": (
            "The learner conflates 'parameters' and 'arguments', treating them as synonyms. "
            "They have not distinguished between the definition-time placeholder (parameter) "
            "and the call-time value (argument)."
        ),
        "trigger_question_ids": ["q_func_002"],
    },
    {
        "concept": "Python Functions",
        "wrong_keywords": ["function", "func", "define", "method"],
        "misunderstanding": (
            "The learner may be drawing from another language (e.g., JavaScript's `function` keyword "
            "or Java's method declarations). They have not yet mapped Python's `def` keyword to the "
            "concept of function definition, suggesting prior language interference."
        ),
        "trigger_question_ids": ["q_func_003"],
    },
    {
        "concept": "Recursion",
        "wrong_keywords": ["stop", "eventually", "automatically", "itself"],
        "misunderstanding": (
            "The learner does not understand that recursion requires an explicit termination condition "
            "(base case). They believe the function will naturally 'know' when to stop, which would "
            "lead to infinite recursion and a stack overflow."
        ),
        "trigger_question_ids": ["q_rec_001"],
    },
    {
        "concept": "List Comprehensions",
        "wrong_keywords": ["loop", "faster", "always", "better"],
        "misunderstanding": (
            "The learner over-generalises that list comprehensions are always preferable to for-loops. "
            "They have not yet understood that when only side effects are needed (no list to build), "
            "a for-loop is the more idiomatic and readable choice."
        ),
        "trigger_question_ids": ["q_lc_003"],
    },
]


def _normalise(text: str) -> str:
    return text.lower().strip()


def _wrong_attempts(attempts: List[Attempt]) -> List[Attempt]:
    return [a for a in attempts if not a.is_correct]


def detect_misconception(
    attempts: List[Attempt],
    current_question_id: str,
    current_answer: str,
    concept_name: str,
    is_correct: bool,
) -> MisconceptionSignal:
    """
    Analyse the learner's history of wrong attempts plus the current answer
    to detect a misconception signal.

    Confidence is computed from:
      - How many times the same error pattern appeared (recurrence)
      - Whether the current answer also matches the pattern
    """
    wrong = _wrong_attempts(attempts)
    normalised_current = _normalise(current_answer)

    best_match: dict | None = None
    best_score: float = 0.0
    recurrence: int = 0

    for pattern in _ERROR_PATTERNS:
        if pattern["concept"].lower() != concept_name.lower():
            continue

        # Count keyword hits across all wrong answers + current answer
        hits = 0
        all_wrong_answers = [_normalise(a.learner_answer) for a in wrong]
        all_wrong_answers.append(normalised_current)

        for wrong_answer in all_wrong_answers:
            if any(kw in wrong_answer for kw in pattern["wrong_keywords"]):
                hits += 1

        if hits > 0:
            # Weight by recurrence; current wrong answer adds extra weight
            current_hit = int(
                any(kw in normalised_current for kw in pattern["wrong_keywords"])
                and not is_correct
            )
            score = min(0.3 * hits + 0.4 * current_hit, 1.0)
            if score > best_score:
                best_score = score
                best_match = pattern
                recurrence = hits

    if best_match and best_score > 0.0 and not is_correct:
        # Clamp: max confidence 0.95 (never 100% certain)
        confidence = min(best_score + 0.1 * min(recurrence, 3), 0.95)
        return MisconceptionSignal(
            detected=True,
            concept_name=concept_name,
            misunderstanding_description=best_match["misunderstanding"],
            confidence_score=round(confidence, 2),
        )

    # No pattern matched or answer was correct
    return MisconceptionSignal(
        detected=False,
        concept_name=concept_name,
        misunderstanding_description=(
            "No recurring misconception detected. The learner answered correctly "
            "or the error does not match a known pattern."
        ),
        confidence_score=0.0,
    )
