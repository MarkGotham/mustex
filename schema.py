"""
Package: `mustex` library for generating latex examples programmatically.

Design: Programmatic here; verbose output so you can fine-tine individual elements.

Use: Experiment with the broad design here; fine-tune there.

Author: Mark Gotham

Licence: MIT

This file: `schema` diagrams

"""

__author__ = "Mark Gotham"


def schema_example(
        root_name: str,
        circles: list[dict],
        include_preamble: bool = False,
        file_name: str = "schema"
) -> None:
    """
    A basic script for generating chord demonstration figures from a list of dicts.
    Each dict gives the name (e.g., "D", "E", "F"), and the tag (int: here, 2, 3, 4).
    Currently, this is hard coded with a root at the bottom (position 0, 0) and others above (0, Y).
    TODO: more flexible options for above, below etc.

    This process include checking that the tags are listed in increasing size and raising an error if not.
    Curved arrows are assigned to the tags alternating left-right- moving from the closest
    and progressively increasing the curvature (bend) as we go to avoid collision.

    :param root_name: The root node is the reference point, so only the name is needed.
    :param circles: A list of dicts with keys for "name" (to be placed in the circle) and "tag" for the annotation.
        The tags should be in size increasing order.
    :param include_preamble: If True, add preamble like `documentclass` and package imports. Defaults to False.
    :param file_name: The file name as a string.
    """

    tags = [circle['tag'] for circle in circles]
    if tags != sorted(tags):
        raise ValueError("Tags must be in increasing order")

    with open(f"./output/{file_name}.tex", "w") as f:

        if include_preamble:
            f.write("\\documentclass[tikz,border=10pt]{standalone}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\usetikzlibrary{shapes.misc, arrows.meta, bending}\n")
            f.write("\\begin{document}\n")

        f.write("\\begin{tikzpicture}\n")

        # Root circle:
        root_string = "{" + root_name + "}"  # Verbose to avoid confusion with f-strings and {} characters
        f.write(f"    \\node (bottom) at (0,0) [circle, fill=black, text=white, minimum width=1.5em] {root_string};\n")

        # Circles above:
        for i, circle in enumerate(circles):
            f.write(
                f"    \\node (top{i + 1}) at (0, {i + 1}) [circle, draw=black, thick, minimum width=1.5em] {{{circle['name']}}};\n")

        # Rounded rectangle around all circles (with the last i defined above:
        f.write(f"    \\draw[rounded corners=5pt, dashed] (-0.5, -0.5) rectangle (0.5, {i + 1.5});\n")

        # Draw curved arrows with annotations:
        f.write("    % Draw curved arrows with annotations\n")
        bend_angle = 0
        for i, circle in enumerate(circles):
            direction = "left" if i % 2 == 0 else "right"
            f.write(
                f"    \\draw[->, bend {direction}={bend_angle}] (bottom) to node[midway, {direction}] {{{circle['tag']}}} (top{i + 1});\n")
            bend_angle += 20

        f.write("\\end{tikzpicture}\n")

        if include_preamble:
            f.write("\\end{document}\n")


def example_use_case() -> None:
    example_root = "C"
    example_upper = [
        {"name": "D", "tag": 2},
        {"name": "E", "tag": 3},
        {"name": "F", "tag": 4},
    ]
    schema_example(example_root, example_upper)


if __name__ == "__main__":
    example_use_case()