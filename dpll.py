from copy import deepcopy


class CNFSAT:
    """
    Class defining the CNF-SAT problem.

    CNF-SAT is the problem whose instances are the formulas of propositional logic that are in Conjunctive Normal Form,
    and an instance is positive if it is satisfiable, i.e. if there exists a valuation for which it is true.
    """
    def __init__(self, clauses: list[set[int]]) -> None:
        """
        Constructs an instance of CNF-SAT.
        
        :param clauses: A list of clauses, where each clause is represented by a set of literals, where the literals
        are represented by integers, with a positive integer `n` representing the propositional variable x_n,
        and a negative  integer `-n` representing the negation of the propositional variable x_n.
        """
        self._clauses = clauses

    def _literals(self) -> set[int]:
        """
        Describes the literals in the formula.

        :return: Returns a *new* set listing every literal present in the formula.
        """
        return set().union(*self._clauses)

    def _find_unit_literal(self) -> int:
        """
        A unit literal is a literal that appears alone in a clause.

        :return: Returns a unit literal if there is one, `None` otherwise; without modifying `self`.
        """
        for c in self._clauses:
            if len(c) == 1:
                return set(c).pop()

    def _find_pure_literal(self) -> int:
        """
        A pure literal is a literal that appears in the formula but whose negation does not.

        :return: Returns a pure literal if there is one, `None` otherwise.
        """
        lits = self._literals()
        for lit in lits:
            if -lit not in lits:
                return lit

    def _unit_propagate(self, lit: int) -> None:
        """
        If `lit` is a unit literal, its value must be set to `True` if `self` is to be satisfied.
        There are thus two operations we can do to simplify `self`:

        - remove all clauses containing `lit`, since `lit` being set to `True` satisfies those clauses;
        - remove the negation of `lit` from all remaining clauses, since `lit` being set to `True` means that the
          negation of `lit` is set to `False`, which prevents it from helping to satisfy those clauses.

        This method will apply this simplification to `self`.

        :param lit: A unit literal.
        """
        self._clauses = [c - {-lit} for c in self._clauses if lit not in c]

    def _pure_literal_assign(self, lit: int) -> None:
        """
        If `lit` is a pure literal, we can drop the clauses that contain it.
        Indeed, if the new formula is satisfiable, by adding (`lit` -> `True`) to a valuation that satisfies the new
        formula, we obtain a valuation that satisfies `self`. Conversely, if `self` is satisfiable, then any valuation
        that satisfies `self` also satisfies the new formula because it is smaller.

        This method will apply this simplification to self.

        :param lit: A pure literal.
        """
        self._clauses = [c for c in self._clauses if lit not in c]

    def _choose_literal_rnd(self) -> int:
        """
        Returns a literal appearing in `self`.

        :return: A literal of `self` if there is any, raises a `KeyError` otherwise.
        """
        return self._literals().pop()

    def dpll(self) -> bool:
        """
        Computes whether `self` is satisfiable.

        :return: `True` if `self` is satisfiable, `False` otherwise.
        """
        if self._clauses == []:
            # If `self` does not have any clause, it is trivially satisfiable.
            return True
        if set() in self._clauses:
            # If `self` has an empty clause, that clause will never be satisfied, so `self` is not satisfiable.
            return False

        # We simplify `self` using the unit propagation rule.
        unit_lit = self._find_unit_literal()
        while unit_lit is not None:
            self._unit_propagate(unit_lit)
            unit_lit = self._find_unit_literal()

        # We simplify `self` using the pure literal rule.
        pure_lit = self._find_pure_literal()
        while pure_lit is not None:
            self._pure_literal_assign(pure_lit)
            pure_lit = self._find_pure_literal()

        # We check again if `self` is trivially satisfiable or trivially non-satisfiable, in case the simplifications
        # helped.
        if not self._clauses:
            return True
        if set() in self._clauses:
            return False

        # If the simplifications were not enough to conclude, we need to make a manual choice. We select a literal
        # appearing in `self`, and we branch on its value: we try to recursively satisfy either the formula where we
        # give it the value `True` or the formula where we give it the value `False`. If either is satisfiable,
        # then `self` is satisfiable. Otherwise, `self` is not satisfiable.
        lit = self._choose_literal_rnd()

        clauses = deepcopy(self._clauses)
        clauses.append({lit})  # We add the clause giving the value `True` to `lit`.
        if CNFSAT(clauses).dpll():
            return True

        self._clauses.append({-lit})  # We add the clause giving the value `False` to `lit`.
        return CNFSAT(self._clauses).dpll()
