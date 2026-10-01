"""
Course-Aware RAG Agent (AI #1) — Learning Outcomes & Taxonomy Parser (Phase 2)
Optimized for Claude 3.5 Sonnet with strict pedagogical calibration & Bloom's Taxonomy.
"""
from __future__ import annotations
import json
import os
import re
from typing import Optional, Dict, Any, List

from Course_Aware_RAG_Agent.models.outcomes_schemas import (
    BloomTaxonomyLevel,
    LearningOutcomeItem,
    CourseOutcomesManifest,
    ParseOutcomesRequest,
)

# ---------------------------------------------------------------------------
# Claude 3.5 Sonnet Prompt Architecture
# ---------------------------------------------------------------------------

def build_claude_outcomes_prompt(
    course_id: str,
    course_title: str,
    syllabus_text: str,
    academic_level: Optional[str] = "Undergraduate"
) -> str:
    """
    Constructs an XML-structured prompt optimized for Claude 3.5 Sonnet to extract,
    calibrate, and format Course Learning Outcomes (CLOs) according to Bloom's Revised Taxonomy.
    """
    prompt = f"""You are the Curriculum & Pedagogy Specialist in the SALI Multi-Agent AI System.
Your task is to analyze course syllabus content, deconstruct it into atomic, measurable Course Learning Outcomes (CLOs / ILOs), and calibrate each outcome precisely against Bloom's Revised Taxonomy.

<context>
  <course_id>{course_id}</course_id>
  <course_title>{course_title}</course_title>
  <academic_level>{academic_level or 'Undergraduate'}</academic_level>
</context>

<bloom_taxonomy_framework>
Every learning outcome must be mapped to one of these 6 cognitive levels:
- "remember": Recall facts and basic concepts (verbs: define, duplicate, list, memorize, repeat, state)
- "understand": Explain ideas or concepts (verbs: classify, describe, discuss, explain, identify, locate, recognize, report, select, translate)
- "apply": Use information in new situations (verbs: execute, implement, solve, use, demonstrate, interpret, operate, schedule, sketch)
- "analyze": Draw connections among ideas (verbs: differentiate, organize, relate, compare, contrast, distinguish, examine, experiment, question, test)
- "evaluate": Justify a stand or decision (verbs: appraise, argue, defend, judge, select, support, value, critique, weigh)
- "create": Produce new or original work (verbs: design, assemble, construct, formulate, author, investigate, develop)
</bloom_taxonomy_framework>

<extraction_rules>
1. Atomicity: Each outcome must represent a single demonstrable capability. Do NOT bundle unrelated skills into one outcome.
2. Action Verb Alignment: The outcome statement must begin with an active, measurable verb corresponding strictly to the chosen bloom_level. Avoid vague verbs like "know", "learn", or "be familiar with".
3. Assessment Rubric Guidance: For each outcome, provide a concrete evaluation guideline explaining how an AI examiner or adaptive quiz agent should test whether a student has mastered this outcome.
4. Target Skills: Extract 2 to 4 specific technical or conceptual competencies required to achieve this outcome.
5. Strict JSON Output: Output ONLY valid JSON complying with the requested schema. Do not enclose in markdown blocks (```json), and include no conversational text before or after.
</extraction_rules>

<target_json_schema>
{{
  "course_id": "{course_id}",
  "course_title": "{course_title}",
  "academic_level": "{academic_level or 'Undergraduate'}",
  "total_outcomes": <integer>,
  "outcomes": [
    {{
      "outcome_id": "CLO-1",
      "title": "<Concise outcome title>",
      "description": "<Student will be able to [measurable action verb] ...>",
      "bloom_level": "remember" | "understand" | "apply" | "analyze" | "evaluate" | "create",
      "action_verbs": ["<verb1>", "<verb2>"],
      "target_skills": ["<skill1>", "<skill2>"],
      "assessment_rubric_hint": "<Guidance for adaptive testing and mastery evaluation>"
    }}
  ]
}}
</target_json_schema>

<raw_syllabus>
{syllabus_text}
</raw_syllabus>

Analyze the syllabus thoroughly, calibrate cognitive depths rigorously, and produce the JSON manifest:"""
    return prompt


# ---------------------------------------------------------------------------
# Claude 3.5 Sonnet Parser Engine
# ---------------------------------------------------------------------------

class ClaudeOutcomesParser:
    """
    Parses course syllabus texts into calibrated CourseOutcomesManifest.
    Integrates directly with Anthropic's Claude 3.5 Sonnet API, with intelligent fallback.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"[ClaudeOutcomesParser] Warning: Could not initialize Anthropic client: {e}")

    def parse(self, request: ParseOutcomesRequest) -> CourseOutcomesManifest:
        """
        Parses the syllabus text into a CourseOutcomesManifest.
        Uses Claude 3.5 Sonnet if client is available; otherwise uses deterministic pedagogical fallback.
        """
        prompt = build_claude_outcomes_prompt(
            course_id=request.course_id,
            course_title=request.course_title,
            syllabus_text=request.syllabus_text,
            academic_level=request.academic_level
        )

        if self.client:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    temperature=0.1,
                    system="You are an expert pedagogical curriculum designer specializing in Bloom's Revised Taxonomy and competency-based education. Output strictly valid JSON matching the schema.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                raw_text = response.content[0].text
                return self._parse_json_response(raw_text, request, model_source=f"claude-3.5-sonnet ({self.model})")
            except Exception as e:
                print(f"[ClaudeOutcomesParser] Claude API call failed: {e}. Falling back to deterministic parser.")

        # Fallback deterministic heuristic parser (offline / without API key)
        return self._fallback_parse(request)

    def _clean_json_str(self, text: str) -> str:
        """Removes markdown code fences and whitespace from LLM output."""
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def _parse_json_response(self, raw_text: str, request: ParseOutcomesRequest, model_source: str) -> CourseOutcomesManifest:
        cleaned_json = self._clean_json_str(raw_text)
        try:
            data = json.loads(cleaned_json)
        except json.JSONDecodeError:
            # Try to regex extract json object
            match = re.search(r"(\{.*\})", cleaned_json, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
            else:
                raise ValueError("Could not parse JSON from Claude response.")

        # Ensure metadata contains model attribution
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["model_engine"] = model_source

        return CourseOutcomesManifest.model_validate(data)

    def _fallback_parse(self, request: ParseOutcomesRequest) -> CourseOutcomesManifest:
        """
        Deterministic, pedagogically-sound fallback parser that analyzes syllabus structure,
        maps keywords to Bloom's taxonomy, and generates calibrated outcomes.
        """
        lines = [line.strip() for line in request.syllabus_text.splitlines() if line.strip()]
        
        bloom_keyword_map = {
            BloomTaxonomyLevel.CREATE: ["design", "create", "build", "develop", "synthesize", "architect", "formulate"],
            BloomTaxonomyLevel.EVALUATE: ["evaluate", "critique", "assess", "justify", "defend", "benchmark", "validate"],
            BloomTaxonomyLevel.ANALYZE: ["analyze", "compare", "differentiate", "examine", "investigate", "deconstruct", "profile"],
            BloomTaxonomyLevel.APPLY: ["implement", "apply", "execute", "solve", "use", "program", "deploy", "trace"],
            BloomTaxonomyLevel.UNDERSTAND: ["explain", "understand", "describe", "discuss", "classify", "summarize", "interpret"],
            BloomTaxonomyLevel.REMEMBER: ["define", "identify", "list", "name", "recall", "state", "recognize"]
        }

        # Detect candidate outcome statements or bullet points
        candidates = []
        for line in lines:
            cleaned = re.sub(r"^[-*•\d\.\)\s]+", "", line).strip()
            if len(cleaned) > 20 and not cleaned.lower().startswith("syllabus") and not cleaned.lower().startswith("instructor"):
                candidates.append(cleaned)

        if not candidates:
            candidates = [
                f"Understand fundamental core principles of {request.course_title}",
                f"Apply algorithmic problem solving and practical implementations in {request.course_title}",
                f"Analyze performance bottlenecks and structural trade-offs in {request.course_title}",
                f"Design and evaluate complex architectures relevant to {request.course_title}"
            ]

        outcomes: List[LearningOutcomeItem] = []
        for i, text in enumerate(candidates[:8], 1):
            lower_text = text.lower()
            assigned_level = BloomTaxonomyLevel.UNDERSTAND
            matched_verbs = []

            # Determine Bloom level based on verb precedence
            matched = False
            for level, keywords in bloom_keyword_map.items():
                for kw in keywords:
                    if kw in lower_text:
                        assigned_level = level
                        matched_verbs.append(kw)
                        matched = True
                        break
                if matched:
                    break

            if not matched_verbs:
                matched_verbs = ["explain", "demonstrate"]

            # Generate rubric hint based on level
            rubric_hints = {
                BloomTaxonomyLevel.REMEMBER: "Provide factual recall multiple-choice question or terminology fill-in.",
                BloomTaxonomyLevel.UNDERSTAND: "Ask student to explain mechanism in their own words or contrast with related ideas.",
                BloomTaxonomyLevel.APPLY: "Present a concrete problem scenario and evaluate code implementation or calculation.",
                BloomTaxonomyLevel.ANALYZE: "Give contrasting architectures or edge-cases and evaluate identification of trade-offs.",
                BloomTaxonomyLevel.EVALUATE: "Require defense or critique of an engineering choice with quantitative justification.",
                BloomTaxonomyLevel.CREATE: "Task student with designing a complete system specification or novel solution."
            }

            outcomes.append(
                LearningOutcomeItem(
                    outcome_id=f"CLO-{i}",
                    title=f"Core Competency: {text[:45]}..." if len(text) > 45 else f"Core Competency: {text}",
                    description=text,
                    bloom_level=assigned_level,
                    action_verbs=matched_verbs,
                    target_skills=[request.course_title, f"Topic-{i}"],
                    assessment_rubric_hint=rubric_hints.get(assigned_level, "Evaluate mastery through targeted questions.")
                )
            )

        manifest = CourseOutcomesManifest(
            course_id=request.course_id,
            course_title=request.course_title,
            academic_level=request.academic_level,
            total_outcomes=len(outcomes),
            outcomes=outcomes,
            metadata={
                "source": "deterministic_pedagogical_engine",
                "target_model": "Claude 3.5 Sonnet",
                "notes": "API key not detected; generated via SALI pedagogical rules engine."
            }
        )
        return manifest
