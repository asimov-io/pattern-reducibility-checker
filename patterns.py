from reductor import PatternReducibility


p_22 = PatternReducibility([[1], [0, 2], [1]], [0, 2], [[0, 1], [1, 0]])
assert(p_22.is_pattern_reducible())

p_232 = PatternReducibility([[1], [0, 2, 3], [1, 3], [1, 2, 4], [3]], [0, 2, 4], [[0, 1, 2], [2, 1, 0]])
assert(p_232.is_pattern_reducible())

p_3_2x3 = PatternReducibility(
     [[1], [0, 2, 3], [1, 3], [1, 2, 4, 8], [3, 5, 6, 8], [4, 6], [4, 5, 7], [6], [3, 4, 9], [8]],
     [0, 2, 5, 7, 9],
     [[0, 1, 2, 3, 4], [3, 2, 1, 0, 4]]
)
assert(p_3_2x3.is_pattern_reducible())

p_233_2x2 = PatternReducibility(
     [[1], [0, 2, 3], [1, 3], [1, 2, 4, 8], [3, 5, 6, 8], [4, 6], [4, 5, 7], [6], [3, 4, 9], [8]],
     [0, 5, 7, 9, 2],
     [[0, 1, 2, 3, 4]]
)
assert(p_233_2x2.is_pattern_reducible())

p_3_2x233_2 = PatternReducibility(
     [
          [1], [0, 2, 3], [1, 3, 4, 6], [1, 2], [2, 5, 6], [4], [2, 4, 7, 8],
          [6, 8], [6, 7, 9, 10], [8, 10], [8, 9, 11], [10]
     ],
     [0, 5, 7, 11, 9, 3],
     [[0, 1, 2, 3, 4, 5]]
)
assert(p_3_2x233_2.is_pattern_reducible())

p_7 = PatternReducibility(
     [
          [14, 1, 2], [0, 2], [0, 1, 3, 4], [2, 4], [2, 3, 5, 7], [4, 6, 7], [5], [4, 5, 8, 10],
          [7, 9, 10], [8], [7, 8, 11, 12], [10, 12], [10, 11, 13, 14], [12, 14], [12, 13, 0]
     ],
     [1, 3, 6, 9, 11, 13],
     [[0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0]]
)
assert(p_7.is_pattern_reducible())

critical_face = PatternReducibility(
     [
          [1, 11], [0, 11, 2, 3], [1, 3], [1, 2, 4], [3, 5, 6], [4, 6], [4, 5, 7, 8],
          [6, 8], [6, 7, 9, 10], [8, 10], [8, 9, 11], [10, 0, 1]
     ],
     [0, 2, 5, 7, 9],
     [[0, 1, 2, 3, 4], [1, 0, 4, 3, 2]]
)
assert(not critical_face.is_pattern_reducible())
