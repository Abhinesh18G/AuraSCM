"""
AuraSCM - Dependency Graph Analyzer
------------------------------------
Builds a call/import graph of a Python module using `ast`, then uses
`networkx` to figure out which functions DEPEND ON a changed function.
This tells us the "blast radius" of a semantic conflict -- i.e. if
`calculate_total()` changes behavior, which other functions/callers
are put at risk.
"""

import ast
import networkx as nx


def build_call_graph(source_code: str) -> nx.DiGraph:
    """
    Build a directed graph: edge (A -> B) means function A calls function B.
    """
    tree = ast.parse(source_code)
    graph = nx.DiGraph()

    function_names = {
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    graph.add_nodes_from(function_names)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            caller = node.name
            for inner in ast.walk(node):
                if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                    callee = inner.func.id
                    if callee in function_names and callee != caller:
                        graph.add_edge(caller, callee)
    return graph


def blast_radius(graph: nx.DiGraph, changed_function: str) -> list:
    """
    Return every function that (directly or transitively) CALLS the
    changed function -- these are the functions at risk of breaking.
    """
    if changed_function not in graph:
        return []
    reversed_graph = graph.reverse()
    reachable = nx.descendants(reversed_graph, changed_function)
    return sorted(reachable)


def dependency_depth(graph: nx.DiGraph, changed_function: str) -> int:
    """How many callers-of-callers deep the impact could ripple."""
    affected = blast_radius(graph, changed_function)
    if not affected:
        return 0
    reversed_graph = graph.reverse()
    lengths = nx.single_source_shortest_path_length(reversed_graph, changed_function)
    return max(lengths.values()) if lengths else 0


if __name__ == "__main__":
    with open("sample_repo/branch_b.py") as f:
        source = f.read()

    g = build_call_graph(source)
    print("Call graph edges:", list(g.edges()))

    affected = blast_radius(g, "calculate_total")
    print(f"\nFunctions affected if `calculate_total` changes behavior: {affected}")
    print(f"Dependency depth: {dependency_depth(g, 'calculate_total')}")
