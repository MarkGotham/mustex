"""
Package: `mustex` library for generating latex examples programmatically.

Design: Programmatic here; verbose output so you can fine-tine individual elements.

Use: Experiment with the broad design here; fine-tune there.

Author: Mark Gotham

Licence: MIT

This file: `cycles` for visualising tonality, meter, and more on circles.

"""

__author__ = "Mark Gotham"

import math
from typing import Optional
from utils import pitch_name_list


# -----------------------------------------------------------------------------

# Set up

def node_strings(
        ks: list[int],
        n: int,
        label_angles: bool = True,
        denominator_in_label: bool = False,
        tonality_not_count: bool = False,
        radius_string: str = "\\radius",
) -> list:
    """
    Abstracts the generation of individual node strings.

    :param ks: The indices of elements in the circle to highlight (full black).
    :param n: The number of elements (equally spaced) in the circle.
    :param label_angles: If True, position the labels precisely with the `label=<angle>:<label text>` syntax.
        If False, use only above, left, right, below.
    :param denominator_in_label: For count label (0, 1, 2, ...),  `1/n` if True; `1` otherwise.
    :param tonality_not_count: If True, check n=12 and if so, use the pitch classes as labels.
    :param radius_string: The variable name for the radius.

    :return: a list of strings
    """

    strings = []

    if tonality_not_count:
        if not n == 12:
            raise ValueError(
                f"To use the pitch class labels, the cycle length (currently {n}) must be 12."
            )

    for i in range(n):

        angle = (360 + 90 - ((i / n) * 360)) % 360

        colour = "black" if (i in ks) else "white"

        if label_angles:
            label_position = angle
        else:
            if i / n == 0:
                label_position = "above"
            elif i / n < 0.5:
                label_position = "right"
            elif i / n == 0.5:
                label_position = "below"
            elif i / n > 0.5:
                label_position = "left"

        if tonality_not_count:  # NB n=12 check is above
            label = pitch_name_list[i]
        else:
            if denominator_in_label:
                label = f"{i}/{n}"
            else:
                label = i

        t = f"\\node (n{i}) at +({angle}:{radius_string}) [circle, draw, fill={colour}, label = {label_position}:{label}]"
        strings.append(
            t + "{};\n"
        )

    return strings


def single_cycle_example(
        ks: list[int],
        n: int,
        radius: float = 1.,
        lines: bool = True,
        adjacent_not_all: bool = True,
        tonality_not_count: bool = False,
        include_preamble: bool = False,
        file_name: str = "cycle_example"
) -> None:
    """
    Draws a single circle with
    k-in-n nodes,
    0/cycle at the top,
    labels positioned above at the top, below at the bottom, left on the left and right on the right.

    TODO possibly add options for multiple sets of ks; all lines and filled/not as the union?

    :param ks: The indices of elements in the circle to highlight (full black).
    :param n: The number of elements (equally spaced) in the circle.
    :param radius: relative scale of circle radius.
    :param lines: If True, include direct lines between elements
    :param tonality_not_count: If True, check n=12 and if so, use the pitch classes as labels.
    :param adjacent_not_all: If True, lines only between adjacent items; if False, lines between all pairs.
    :param include_preamble: If True, add preamble like `documentclass` and package imports. Defaults to False.
    :param file_name: The file name as a string.
    """
    if ks is None:
        ks = range(n)
    else:
        for k in ks:
            if k not in range(n):
                raise ValueError(f"Highlighted index {k} is greater than the total n ({n}).")

    with open(f"./output/{file_name}.tex", "w") as f:

        if include_preamble:
            f.write("\\documentclass[tikz,border=10pt]{standalone}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\usetikzlibrary{shapes.misc, arrows.meta, bending}\n")
            f.write("\\begin{document}\n")

        scale = int(math.log2(n) - 1)  # E.g., 2 for n=8, 3 for n = 16

        f.write("\\begin{tikzpicture}[scale={" + str(scale) + "}]\n")

        # Circle
        f.write("\def \\radius{" + str(radius) + "}\n")
        f.write("\\node (origin) at (0,0) {};\n")
        f.write("\draw (origin) circle (\\radius);\n")

        nodes = node_strings(ks, n, tonality_not_count=tonality_not_count) # default radius_string
        for n in nodes:
            f.write(n)

        if lines:
            if adjacent_not_all:
                for i in range(len(ks) - 1):
                    f.write(f"\draw[solid] (n{ks[i]}) -- (n{ks[i + 1]});\n")
                # Last one:
                f.write(f"\draw[solid] (n{ks[-1]}) -- (n0);\n")
            else:
                from itertools import combinations
                c = combinations(ks, 2)
                for pair in c:
                    f.write(f"\draw[solid] (n{pair[0]}) -- (n{pair[1]});\n")

        f.write("\\end{tikzpicture}\n")

        if include_preamble:
            f.write("\\end{document}\n")


def two_circles(
        inner_k: Optional[list[int]] = None,
        inner_n: int = 3,
        inner_radius: float = 1.5,
        outer_k: Optional[list[int]] = None,
        outer_n: int = 8,
        outer_radius: float = 2.,
        include_preamble: bool = False,
        file_name: str = "double_cycle"
) -> None:
    """
    As for single_cycle_example, but with 2x k-in-n cycles (inner and outer).

    :param inner_n: The number of elements (equally spaced) in the inner circle.
    :param inner_k: The elements of the inner circle to highlight (full black).
    :param inner_radius: relative scale of inner circle radius.

    :param outer_n: The number of elements (equally spaced) in the inner circle.
    :param outer_k: The elements of the inner circle to highlight (full black).
    :param outer_radius: relative scale of outer circle radius.
    :param file_name: The file name as a string.

    :param include_preamble: If True, add preamble like `documentclass` and package imports. Defaults to False.
    """

    # Checks
    if inner_k is None:
        inner_k = range(inner_n)
    else:
        for k in inner_k:
            if k not in range(inner_n):
                raise ValueError(f"Highlighted index {k} is greater than the total n ({inner_n}).")

    if outer_k is None:
        outer_k = range(outer_n)
    else:
        for k in outer_k:
            if k not in range(outer_n):
                raise ValueError(f"Highlighted index {k} is greater than the total n ({outer_n}).")

    with open(f"./output/{file_name}.tex", "w") as f:

        if include_preamble:
            f.write("\\documentclass[tikz,border=10pt]{standalone}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\usetikzlibrary{shapes.misc, arrows.meta, bending}\n")
            f.write("\\begin{document}\n")

        f.write("\\begin{tikzpicture}[scale=2]\n")

        # Inner Circle
        f.write("\def \\innerradius{" + str(inner_radius) + "}\n")
        f.write("\\node (origin) at (0,0) {};\n")
        f.write("\draw (origin) circle (\\innerradius);\n")
        nodes = node_strings(inner_k, inner_n, radius_string="\\innerradius")
        for n in nodes:
            f.write(n)

        # Outer Circle
        f.write("\def \\outerradius{" + str(outer_radius) + "}\n")
        f.write("\\node (origin) at (0,0) {};\n")
        f.write("\draw (origin) circle (\\outerradius);\n")
        nodes = node_strings(outer_k, outer_n, radius_string="\\outerradius")
        for n in nodes:
            f.write(n)

        f.write("\\end{tikzpicture}\n")

        if include_preamble:
            f.write("\\end{document}\n")


# -----------------------------------------------------------------------------

# Specific examples

def tresillo_example() -> None:
    single_cycle_example(
        ks=[0,3,6],
        n=8,
        radius=1.,
        lines=True,
        file_name="tresillo"
    )


def double_tresillo_all_intervals() -> None:
    single_cycle_example(
        ks=[0, 3, 6, 8, 11, 14],
        n=16,
        lines=True,
        adjacent_not_all=False,
        file_name="double_tresillo_all_intervals"
    )


def tonality_example() -> None:
    single_cycle_example(
        # ks=[0,2,4,5,7,9,11],
        ks=[2, 5, 8, 11],
        n=12,
        radius=1.,
        tonality_not_count=True,
        lines=True,
        adjacent_not_all=False,
        file_name="tonality"
    )

def two_circles_3_in_8() -> None:
    two_circles(
        inner_k=None,
        inner_n=3,
        outer_k=[0,3,5],
        outer_n=8,
        file_name="two_circles_3_in_8"
    )
# TODO consider calculating and draw nearest lines as part of this.


if __name__ == "__main__":
    tresillo_example()
    double_tresillo_all_intervals()
    tonality_example()
    two_circles_3_in_8()
