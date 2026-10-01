"""
Course-Aware RAG Agent (AI #1) — Concept Graph Storage (Phase 3)
Persists CourseConceptGraph JSON files to disk.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from Course_Aware_RAG_Agent.models.concept_graph_schemas import CourseConceptGraph


class ConceptGraphStorage:
    def __init__(self, storage_dir: Optional[Path] = None):
        if storage_dir is None:
            self.storage_dir = Path(__file__).resolve().parent.parent / "data" / "concept_graphs"
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, course_id: str) -> Path:
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in course_id)
        return self.storage_dir / f"{safe_name}_graph.json"

    def save_graph(self, graph: CourseConceptGraph) -> Path:
        file_path = self._get_path(graph.course_id)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(graph.model_dump_json(indent=2))
        return file_path

    def get_graph(self, course_id: str) -> Optional[CourseConceptGraph]:
        file_path = self._get_path(course_id)
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return CourseConceptGraph.model_validate(data)

    def list_graphs(self) -> List[Dict[str, Any]]:
        results = []
        for file in self.storage_dir.glob("*_graph.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results.append({
                    "course_id": data.get("course_id"),
                    "course_title": data.get("course_title"),
                    "nodes_count": len(data.get("nodes", [])),
                    "edges_count": len(data.get("edges", [])),
                    "is_dag": data.get("is_dag", True),
                    "learning_steps": len(data.get("topological_learning_path", [])),
                    "file_name": file.name
                })
            except Exception:
                continue
        return results
