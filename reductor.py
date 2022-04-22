from utils import *
from coloring import ThreeColoration
from aux_graph import NCPQMatching


class PatternReducibility:
    """
    Class defining the Pattern Reducibility problem.

    Pattern Reducibility is the problem whose instances are patterns, and an instance is positive if it is reducible.
    """
    def __init__(self, line_graph: list[list[int]], outgoing: list[int], symmetries: list[list[int]]) -> None:
        """
        Constructs an instance of `PatternReducibility`.

        :param line_graph: Line graph of the pattern, given by adjacency list.
        :param outgoing: List of outgoing vertices (vertices of the line graph corresponding to outgoing edges of the
            graph) in a cyclic order.
            !! WARNING !! The outgoing vertices must be numbered cyclically.

        :param symmetries: List of symmetries of the outgoing vertices.
            !! WARNING !! It must start with the identity.

        :Example:

        See the patterns.py file for examples.
        """
        self.line_graph = line_graph
        self.outgoing = outgoing
        self.k = len(outgoing)
        self.symmetries = symmetries

        # We use the word "coloring" as a shorthand for "frontier coloring" when the context makes it clear.

        # Two colorings are color-equivalent if they are equal up to a color permutation;
        # the color-representative of a coloring is the lexicographically minimal color-equivalent of that coloring.

        # Similarly, two colorings are equivalent if they are equal up to a color permutation and a symmetry;
        # and the representative of a coloring is the lexicographically minimal equivalent of that coloring.

        # Maps the representatives of the colorings to their reducibility and rank.
        self.repr_to_red = {}

        # The following two objects are used to determine which colorings are representatives.

        # First layer maps each coloring to its color-representative.
        # The color-representatives are the colorings that are their own color-representative.
        self.color_repr_map = {}

        # Second layer only considers the color-representatives for its keys.
        # It maps a color-representative to its representative.
        # The representatives are the colorings that are their own representative.
        self.repr_map = {}

        # We filter the colorings that are color-representatives.
        for c in colorings(self.k):
            # We compute the color-representative of `c` and store it.
            self.color_repr_map[c] = color_repr(c)
            if self.color_repr_map[c] == c:
                # `c` is a color-representative, so we add it as a potential representative.
                self.repr_map[c] = None

        # We filter the color-representatives that are representatives.
        for c in self.repr_map.keys():
            # For every coloring reachable from `c` by using a symmetry of the pattern, we consider its
            # color-representative, and the lowest of those is the representative of `c`.
            self.repr_map[c] = min((self.color_repr_map[c_sym] for c_sym in
                                    (tuple(c[i] for i in sym) for sym in self.symmetries)),
                                   key=coloring_to_int)
            if self.repr_map[c] == c:
                # `c` is a representative, so we want to compute its reducibility and rank. The first step is to
                # check if it is extendable into a coloring, and put the result in the `self.repr_to_red` mapping.

                # We build the `ThreeColoration` instance from the line graph by adding the constraints from `c`:
                if ThreeColoration(self.line_graph, {self.outgoing[i]: c[i] for i in range(self.k)}).colorable():
                    # The frontier coloring `c` is extendable into a coloring, so it is reducible, of rank 0.
                    self.repr_to_red[c] = {"rank": 0, "reason": "extendable"}
                else:
                    # The frontier coloring `c` is not extendable into a coloring.
                    # We do not know yet if it is reducible. For now, it is considered non-reducible.
                    self.repr_to_red[c] = {"rank": float("inf"), "reason": ""}

    def _representative(self, c: tuple[Color, ...]) -> tuple[Color, ...]:
        """
        Returns the representative of a coloring.

        :param c: A coloring represented by a tuple of colors.
        :return: The lexicographically minimal coloring equal to `c` up to a color permutation and a symmetry.
        """
        return self.repr_map[self.color_repr_map[c]]

    def _make_aux_graph(self, c: tuple[Color, ...], r: int, color_pair: tuple[Color, Color]):
        """
        Returns the auxiliary graph of `c` with respect to Γ and `color_pair` where Γ is the set of the colorings
        that are already proven of rank < `r`, i.e. Γ = {`c'` coloring such that `self.repr_to_red[c']["rank"] < r`}.

        :param c: A coloring represented by a tuple of colors.
        :param r: A rank.
        :param color_pair: A pair of colors represented by a tuple of two colors.
        :return: The auxiliary graph of `c` with respect to the set of known colorings of rank < `r` and `color_pair`,
        as an instance of `NCPQMatching`.
        """
        def swap(indices: set[int]) -> tuple[Color, ...]:
            """
            Switches the colors of the outgoing vertices listed in `indices`.

            :param indices: One or two distinct outgoing vertices, given by a set of integers.
            :return: The coloring obtained from `c` by switching the color assigned to the outgoing vertices
            listed in `indices` from i to j or j to i, where (i, j) = `color_pair`.
            """
            res = list(c)
            for index in indices:
                if res[index] == color_pair[0]:
                    res[index] = color_pair[1]
                elif res[index] == color_pair[1]:
                    res[index] = color_pair[0]
            return tuple(res)

        # `g` represents the auxiliary graph as a mapping from each vertex to its adjacency set.
        g = {}
        for i in range(self.k):
            if c[i] in color_pair:
                # If the `i`-th outgoing edge has a color from `color_pair`, we add `i` as a vertex of `g`.
                g[i] = set()

        for u in g.keys():
            for v in g.keys():
                # If `u` = `v`, `{u, v}` = `{u}` and we only swap the edge indexed by `u`.
                if self.repr_to_red[self._representative(swap({u, v}))]["rank"] >= r:
                    # We follow the rules given in definition 2.4 for adding edges and loops.
                    g[u].add(v)
                    g[v].add(u)
        return NCPQMatching(g)

    def _is_coloring_reducible(self, c: tuple[Color, ...], r: int):
        """
        Determines whether coloring `c` is reducible to the set of known colorings of rank < `r`.

        :param c: A coloring represented by a tuple of colors.
        :param r: A rank.
        :return: `{"reducible": True, "color pair": (i, j)}` if `c` is proven reducible using color pair `(i, j)`,
        or `{"reducible": False, "color pair": ()}` if no color pair can achieve this.
        """
        for color in range(1, 4):
            # We consider the Kempe chains using the two colors that are not `color`.
            color1, color2 = {1, 2, 3} - {color}
            if c != tuple(Color(color) for _ in range(self.k)):
                # We do not consider the case where the auxiliary graph is empty — it is trivially matchable.
                aux_graph = self._make_aux_graph(c, r, (Color(color1), Color(color2)))
                if not aux_graph.matchable():
                    return {"reducible": True, "color pair": (color1, color2)}
        return {"reducible": False, "color pair": ()}

    def is_pattern_reducible(self, display=False) -> bool:
        """
        Computes the rank of every representative coloring of the pattern.

        :param display: Boolean value that defaults to `False`. If set to `True`, the method will display the reducible
        colorings, distributed among the various ranks, with a last category containing the non-reducible ones.
        :return: `True` if the pattern is reducible (every representative coloring is reducible), `False` otherwise.
        """
        found_changed = True
        i = 1

        # Main loop. After the `i`-th iteration, every coloring `c` of rank <= `i` has its correct rank inscribed in
        # `self.repr_to_red[c]["rank"]`.
        while found_changed:
            found_changed = False
            found_non_reducible = False

            # For each representative coloring `c`:
            for c in self.repr_to_red.keys():
                if self.repr_to_red[c]["rank"] == float("inf"):  # If `c` is not known to be reducible:
                    # We re-check with our knowledge of colorings of rank < `i`.
                    res = self._is_coloring_reducible(c, i)
                    if res["reducible"]:
                        found_changed = True  # At least one coloring of rank `i` has been found.
                        self.repr_to_red[c]["rank"] = i
                        color_pair = res["color pair"]
                        self.repr_to_red[c]["reason"] = f"reducible with color pair " \
                                                        f"{str(color_pair[0])}/{str(color_pair[1])}"
                    else:
                        found_non_reducible = True  # At least one coloring of rank > `i` has been found.

            i += 1

        if display:
            # The last rank attributed to a coloring is `i - 2`.
            for r in range(i - 1):
                # Filters the representatives of rank `r`.
                rank_r = [(c, red) for (c, red) in self.repr_to_red.items() if red["rank"] == r]
                nb_r = len(rank_r)
                print(f"\nThere {'are' * (nb_r != 1)}{'is' * (nb_r == 1)} {nb_r} coloration{'s' * (nb_r != 1)}"
                      f" of rank {r}:\n")
                for c, red in rank_r:
                    print(f"{tuple(map(int,c))} because {red['reason']}.")

            print("\nNon reducible colorations:\n")
            for c, red in self.repr_to_red.items():
                if red["rank"] == float("inf"):
                    print(c)
        return not found_non_reducible
