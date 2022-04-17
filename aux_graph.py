from dpll import CNFSAT


class NCPQMatching:
    """
    Class defining the Non-Crossing Perfect Quasi-Matching problem.

    Non-Crossing Perfect Quasi-Matching (NCPQM) is the problem whose instances are the plane-embedded pseudo-graphs,
    and an instance is positive if it admits a non-crossing perfect quasi-matching. Here we restrict ourselves to
    certain instances where the plane embedding is deduced from the pseudo-graph itself (see the documentation of the
    `__init__` method).
    """

    def __init__(self, pseudo_graph: dict[int, set[int]]) -> None:
        """
        Constructs an instance of NCPQM from a pseudo-graph.

        :param pseudo_graph: A pseudo-graph represented by a dictionary mapping each vertex to its set of neighbours.

        !! WARNING !! Assumes that the vertices are disposed on a circle in order of value, that loops do not cross any
        edge, and that edges between two vertices are straight lines.
        """
        self._graph = pseudo_graph  # Vertices of the pseudo-graph are positive integers.
        self._edges = {(min(u, v), max(u, v)) for u, neigh in pseudo_graph.items() for v in neigh}  # The edges of
        # the pseudo-graph.

    @staticmethod
    def _crossing(edge1: tuple[int, int], edge2: tuple[int, int]) -> bool:
        """
        Computes whether two edges of `self` are crossing.

        :param edge1: An edge of `self`, represented as a tuple containing 2 integers.
        :param edge2: Idem.
        :return: `True` if `edge1` and `edge2` are crossing, `False` otherwise.
        """
        u1, v1 = edge1
        u2, v2 = edge2
        return (u1 - u2) * (u1 - v2) * (v1 - u2) * (v1 - v2) < 0

    def _var(self, u: int, v: int) -> int:
        """
        The propositional variable x_{u, v} represents edge {u, v} being selected for the matching.

        {u, v} must be an edge of the pseudo-graph.

        :param u: A vertex of `self`.
        :param v: Idem.
        :return: Returns the (injective) integer representation of x_{u, v}.
        """
        assert((min(u, v), max(u, v)) in self._edges)
        bound = max(self._graph.keys()) + 1  # Strictly greater than the difference between any two vertices.
        # Bound is used to ensure the representation is injective:
        return bound * min(u, v) + max(u, v)

    def _formula(self) -> CNFSAT:
        """
        This is a polynomial reduction from NCPQM to CNF-SAT.

        :return: A boolean formula in Conjunctive Normal Form that is
        satisfiable if and only if `self` is a positive instance of NCPQM, i.e.
        `self` has a non-crossing perfect quasi-matching.
        The propositional variables will be the x_{u, v} for {u, v} edge of `self`.
        """
        # We build the clauses of the boolean formula.
        clauses = []

        # For each vertex `u`:
        for u in self._graph.keys():
            # - `u` must see at most one edge (quasi-matching).
            # For any two distinct adjacent vertices `v` and `v2`:
            for v in self._graph[u]:
                for v2 in self._graph[u]:
                    if v != v2:
                        # This clause prevents `u` from seeing both {`u`, `v`} and {`u`, `v2`}:
                        clauses.append({-self._var(u, v), -self._var(u, v2)})

            # - `u` must be covered by the matching (perfect).
            # This clause forces `u` to see at least one edge:
            clauses.append({self._var(u, v) for v in self._graph[u]})

        # For each pair of edges:
        for (u1, v1) in self._edges:
            for (u2, v2) in self._edges:
                if NCPQMatching._crossing((u1, v1), (u2, v2)):  # `(u1, v1)` and `(u2, v2)` are crossing
                    # This clause prevents choosing both (non-crossing):
                    clauses.append({-self._var(u1, v1), -self._var(u2, v2)})
        return CNFSAT(clauses)

    def matchable(self) -> bool:
        """
        Computes whether `self` is a positive instance of NCPQM.

        :return: `True` if there exists a non-crossing perfect quasi-matching of `self`, `False` otherwise.
        """
        return self._formula().dpll()
