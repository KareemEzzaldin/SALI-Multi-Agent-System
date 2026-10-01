"""
Course-Aware RAG Agent (AI #1) — Outcomes Storage
Persists CourseOutcomesManifest JSON files to disk.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from Course_Aware_RAG_Agent.models.outcomes_schemas import CourseOutcomesManifest


class OutcomesStorage:
    def __init__(self, storage_dir: Optional[Path] = None):
        if storage_dir is None:
            self.storage_dir = Path(__file__).resolve().parent.parent / "data" / "outcomes"
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_course_path(self, course_id: str) -> Path:
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in course_id)
        return self.storage_dir / f"{safe_name}.json"

    def save_manifest(self, manifest: CourseOutcomesManifest) -> Path:
        file_path = self._get_course_path(manifest.course_id)
        # Dump using Pydantic v2 model_dump_json
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(manifest.model_dump_json(indent=2))
        return file_path

    def get_manifest(self, course_id: str) -> Optional[CourseOutcomesManifest]:
        file_path = self._get_course_path(course_id)
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return CourseOutcomesManifest.model_validate(data)

    def list_manifests(self) -> List[Dict[str, Any]]:
        results = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results.append({
                    "course_id": data.get("course_id"),
                    "course_title": data.get("course_title"),
                    "total_outcomes": data.get("total_outcomes", len(data.get("outcomes", []))),
                    "academic_level": data.get("academic_level"),
                    "file_name": file.name
                })
            except Exception:
                continue
        return results
