# Pattern Reducibility Checker

This project is the official code for [this paper on 3-edge-coloring of subcubic
planar graphs](https://arxiv.org/abs/2108.06115v1).

## General info

This project was born from the desire to automate the method determining whether
a pattern is *reducible* or not.

* It was thus useful during our work as a preprocessing tool allowing us to
focus our attention on patterns that were deemed reducible by this tool.
* It can still be used to check whether there is another (smaller ?) set
of (smaller ?) reducible patterns that covers planar graphs (i.e. every planar
graph must contain at least one of those patterns).
* Outside the scope of the paper itself, this tool can be more generally useful
for any research that re-uses our definition of *reducibility* for a pattern.

## Project structure

### patterns.py

This file encodes the six reducible patterns used in the proof of the result,
as well as the *critical face* pattern, and asserts that only the critical face
pattern is not reducible.

It serves as a guideline to show how to check patterns.

It runs using the code from the [reductor.py](#reductorpy) file.

### reductor.py

This file is the main file of the project, with the
`PatternReducibility` class implementing the reducibility checker with the
help of the `ThreeColoration` class from [coloring.py](#coloringpy) for
the base case of reducibility and the `NCPQMatching` class from 
[aux_graph.py](#aux_graphpy) for the recursive case.

### coloring.py

This file implements the `ThreeColoration` class that checks whether an
input graph with given color constraints is 3-vertex-colorable, using a
reduction to the CNF-SAT problem to benefit from the DPLL algorithm
implemented in [dpll.py](#dpllpy).

### aux_graph.py

This file implements the `NCPQMatching` class that checks whether an
input pseudo-graph with inferred plane-embedding has a non-crossing
perfect quasi-matching, using here again a reduction to the CNF-SAT
problem to benefit from the DPLL algorithm implemented in
[dpll.py](#dpllpy).

### dpll.py

This file implements the `CNFSAT` class that checks whether an input
propositional formula in Conjunctive Normal Form is satisfiable, using the
Davis-Putnam-Logemann-Loveland algorithm.

### utils.py

This file implements several basic components used in
[coloring.py](#coloringpy) and [reductor.py](#reductorpy).

## Getting started

This project needs Python 3.10 to run.

* To check the reducibility of the patterns presented in the paper, just
run the pattern.py file, adding the `True` argument to
`is_pattern_reducible` if a listing of the different representative
colorings and their rank is needed.
* To add other patterns, check out the syntax defined in
reductor.py and the examples in pattern.py.