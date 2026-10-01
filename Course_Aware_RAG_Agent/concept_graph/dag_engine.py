"""
Course-Aware RAG Agent (AI #1) — DAG Validation & Topological Sequencing Engine (Phase 3)
Employs NetworkX for cycle detection, topological sorting, and pedagogical path sequencing.
"""
from __future__ import annotations
from typing import List, Tuple, Dict, Any
import networkx as nx

from Course_Aware_RAG_Agent.models.concept_graph_schemas import (
    ConceptNode,
    ConceptEdge,
    ConceptRelationType,
    CourseConceptGraph,
)


class DAGEngine:
    """
    Validates, analyzes, and sequences academic concept graphs.
    Guarantees acyclic properties required for linear or branched adaptive learning paths.
    """

    @classmethod
    def analyze_and_sequence(
        cls,
        course_id: str,
        course_title: str,
        nodes: List[ConceptNode],
        edges: List[ConceptEdge],
        metadata: Dict[str, Any] | None = None
    ) -> CourseConceptGraph:
        """
        Builds a NetworkX DiGraph from the concepts and prerequisite edges,
        detects any cycles, computes topological sorting, and identifies entry/capstone nodes.
        """
        G = nx.DiGraph()

        # Add all concept nodes
        node_id_set = set()
        for node in nodes:
            G.add_node(node.concept_id, data=node)
            node_id_set.add(node.concept_id)

        # Filter edges to only valid node IDs and add prerequisite relations
        prereq_edges = []
        for edge in edges:
            if edge.source_id in node_id_set and edge.target_id in node_id_set:
                # In educational DAG: Source is PREREQUISITE_OF Target -> Edge goes Source -> Target
                if edge.relation_type in (ConceptRelationType.PREREQUISITE_OF, ConceptRelationType.EXTENDS):
                    G.add_edge(edge.source_id, edge.target_id, weight=edge.weight)
                    prereq_edges.append(edge)

        # Cycle detection
        is_dag = nx.is_directed_acyclic_graph(G)
        detected_cycles: List[List[str]] = []

        if not is_dag:
            try:
                # Extract simple cycles
                raw_cycles = list(nx.simple_cycles(G))
                detected_cycles = [list(c) for c in raw_cycles[:10]]
                # Pedagogical resolution: remove backward edges to form a valid learning path
                for cycle in raw_cycles:
                    if len(cycle) >= 2 and G.has_edge(cycle[-1], cycle[0]):
                        G.remove_edge(cycle[-1], cycle[0])
            except Exception:
                pass

        # Compute topological learning path
        try:
            topological_path = list(nx.topological_sort(G))
        except Exception:
            # Fallback to order of nodes
            topological_path = [node.concept_id for node in nodes]

        # Root concepts: In-degree == 0 (no prerequisites needed, starting points)
        root_concepts = [n for n in topological_path if G.in_degree(n) == 0]

        # Terminal concepts: Out-degree == 0 (capstone or final topics)
        terminal_concepts = [n for n in topological_path if G.out_degree(n) == 0]

        return CourseConceptGraph(
            course_id=course_id,
            course_title=course_title,
            nodes=nodes,
            edges=edges,
            is_dag=is_dag,
            topological_learning_path=topological_path,
            detected_cycles=detected_cycles,
            root_concepts=root_concepts,
            terminal_concepts=terminal_concepts,
            metadata=metadata or {}
        )
