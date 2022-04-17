from utils import Color
from dpll import CNFSAT


class ThreeColoration:
    """
    Class defining the 3-Coloration problem.

    3-Coloration is the problem whose instances are the partially colored graphs, and an instance is positive if the
    coloration is extendable into a 3-coloration of the graph.
    """
    def __init__(self, adj: list[list[int]], constraints: dict[int, Color] = None):
        """
        Constructs an instance of 3-Coloration.

        :param adj: The adjacency list of the graph.
        :param constraints: A dictionary of (vertex to color) constraints.

        :Example:

        ThreeColoration([[1], [0, 2, 3], [1, 3], [1, 2, 4, 8], [3, 5, 6, 8], [4, 6], [4, 5, 7], [6], [3, 4, 9], [8]],
                 {0: Color.ONE, 2: Color.ONE, 5: Color.ONE, 7: Color.ONE, 9: Color.TWO})
        """
        self._n = len(adj)
        self._constraints = constraints
        self._edges = {frozenset((u, v)) for u in range(self._n) for v in adj[u]}

    def _var(self, vertex: int, color: int):
        """
        The propositional variable x_{vertex, color} represents `vertex` being colored by `color`.

        :param vertex: A vertex of the graph (`0 <= vertex < self._n`).
        :param color: A color (`color` must be in {1, 2, 3}).
        :return: Returns the (injective) integer representation of x_{vertex, color}.
        """
        assert(0 <= vertex < self._n and 1 <= color <= 3)
        return 3 * vertex + color

    def _formula(self) -> CNFSAT:
        """
        This is a polynomial reduction from 3-Coloration to 3-SAT.

        :return: A boolean formula in Conjunctive Normal Form that is
        satisfiable if and only if `self` is a positive instance of 3-Coloration.
        The propositional variables will be the x_{u, c} for u vertex of `self` and c color of {1, 2, 3}.
        """
        # We build the clauses of the boolean formula.
        clauses = []

        for u in range(self._n):
            color = int(self._constraints.get(u, Color.NONE))
            if color != 0:  # We already fixed the color of `u`.
                # This clause forces `u` to be colored by `color`:
                clauses.append({self._var(u, color)})
                for other_color in {1, 2, 3} - {color}:
                    # This clause prevents `u` from being colored by `other_color`:
                    clauses.append({-self._var(u, other_color)})

            else:
                # This clause forces `u` to be colored by at least one color from {1, 2, 3}:
                clauses.append({self._var(u, 1), self._var(u, 2), self._var(u, 3)})
                # These clauses prevent `u` from being colored by two colors at once:
                clauses.append({-self._var(u, 1), -self._var(u, 2)})
                clauses.append({-self._var(u, 1), -self._var(u, 3)})
                clauses.append({-self._var(u, 2), -self._var(u, 3)})

        for (u, v) in self._edges:
            for color in {1, 2, 3}:
                # This clause prevents `u` and `v` from being both colored by `color`:
                clauses.append({-self._var(u, color), -self._var(v, color)})
        return CNFSAT(clauses)

    def colorable(self) -> bool:
        """
        Computes whether `self` is a positive instance of 3-Coloration.

        :return: `True` if there exists a 3-coloration of `self` respecting the input constraints, `False` otherwise.
        """
        return self._formula().dpll()
