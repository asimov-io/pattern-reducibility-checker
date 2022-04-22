from enum import IntEnum
from itertools import product, permutations


class Color(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    NONE = 0


def colorings(n: int):
    """
    Enumerates the colorations of `n` vertices.

    :param n: The number of vertices to be colored.
    :return: A generator enumerating the `n`-tuples composed of colors 1 to 3.
    """
    return product([Color.ONE, Color.TWO, Color.THREE], repeat=n)


def color_permutations():
    """
    Enumerates the 6 color permutations.

    :return: A generator enumerating the 6 permutations of the 3 colors.
    """
    for sigma in permutations((1, 2, 3), 3):
        yield {Color(i + 1): Color(sigma[i]) for i in range(3)}


def permute(coloring: tuple[Color, ...], sigma: dict[Color, Color]) -> tuple[Color, ...]:
    """
    Composes a permutation with a coloring.

    :param coloring: A coloring represented by a tuple of colors.
    :param sigma: A color permutation represented by a `Color` -> `Color` mapping.
    :return: The coloring `sigma` circle `coloring`.
    """
    return tuple(sigma[c] for c in coloring)


def coloring_to_int(coloring: tuple[Color, ...]) -> int:
    """
    Computes the integer representation of `coloring`.

    :param coloring: A coloring represented by a tuple of colors.
    :return: The integer representation of `coloring`.
    """
    return int("".join([str(int(color)) for color in coloring]))


def color_repr(coloring: tuple[Color, ...]) -> tuple[Color, ...]:
    """
    Computes the lexicographically minimal coloring equal to `coloring` up to color permutation.

    :param coloring: A coloring represented by a tuple of colors.
    :return: The minimum color permutation of `coloring` according to the lexicographic order.
    """
    return min((permute(coloring, sigma) for sigma in color_permutations()),
               key=coloring_to_int)
