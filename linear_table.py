"""
Package: `mustex` library for generating latex examples programmatically.

Design: Programmatic here; verbose output so you can fine-tine individual elements.

Use: Experiment with the broad design here; fine-tune there.

Author: Mark Gotham

Licence: MIT

This file: `linear_table` for MIDI <> pitch-class comparison and grid-tatum demonstration

"""

__author__ = "Mark Gotham"

from utils import pitch_name_list


# -----------------------------------------------------------------------------

def midi_pitch_pc_table(
        start_octave: int = 4,
        end_octave: int = 6,
        file_name: str = "midi",
        include_preamble: bool = False,
        open_ended: bool = False
):
    """
    Create a MIDI, pitch name, pitch class comparison table of a certain number of octaves.

    :param start_octave: The first octave to include
    :param end_octave:  The last octave to include (yes, last octave inclusive).
    :param file_name: The directory `./output/` is hard-coded. Name here.
    :param include_preamble: Start `documentclass{standalone}` or `begin{tabular}`.
    :param open_ended: If True, start and end with an ellipsis; if False label the rows.
    :return:
    """
    ints = range(start_octave * 12, end_octave * 12)
    if open_ended:
        d = ["\\dots"]  # For the ends
    else:
        d = [""]
    midis = " & ".join(d + [str(x) for x in ints] + d)
    octaves = end_octave - start_octave
    pcs = " & ".join(d + [str(x) for x in list(range(12)) * octaves] + d)
    names = " & ".join(d + (pitch_name_list * octaves) + d)
    ccs = "c" + ("|cccccccccccc" * octaves) + "|c"  # TODO consider p{4pt}

    with open(f"./output/{file_name}.tex", "w") as f:

        if include_preamble:
            f.write("\\documentclass{standalone}\n")
            f.write("\\begin{document}\n")
            f.write("\\begin{table}[h!]\n")
            f.write("\\centering\n")
            f.write("\\caption{MIDI Pitch to Pitch Class Mapping}\n")

        f.write("\\begin{tabular}{" + ccs + "}\n")

        if not open_ended:
            f.write("\\textbf{MIDI} ")
        f.write(midis + "\n")
        f.write("\\\\\n")

        if not open_ended:
            f.write("\\textbf{Name} ")
        f.write(names + "\n")
        f.write("\\\\\n")

        if not open_ended:
            f.write("\\textbf{Class} ")
        f.write(pcs + "\n")
        f.write("\\end{tabular}\n")


def grid_tatum(
        n_divs: int = 5,
        length_unit: int = 8,
        file_name: str = "grid_tatum",
        include_preamble: bool = False,
):
    """
    Create a demonstration of grid/tatum with 1/n divisions of a span.

    :param n_divs: How many divisions (1/1, 1/2, ... 1/n).
    :param length_unit: The unit length for the whole.
    :param file_name: The directory `./output/` is hard-coded. Name here.
    :param include_preamble: Start `documentclass{standalone}` or `begin{tabular}`.
    :return:
    """
    with open(f"./output/{file_name}.tex", "w") as f:

        if include_preamble:
            f.write("\\documentclass{standalone}\n")
            f.write("\\begin{document}\n")
            f.write("\\begin{table}[h!]\n")
            f.write("\\centering\n")

        f.write("\\begin{tikzpicture}[scale=1, transform shape]\n")

        for n in range(n_divs):
            for i in range(n):
                f.write(f"\\filldraw[fill=blue!20, draw=black]")
                f.write(f"({length_unit * i / n}, {n})")  # Bottom left
                f.write(f"rectangle ({(i + 1) * length_unit / n}, {n + 1})")  # Top right
                f.write("node[midway] {1/")
                f.write(str(n))  # Label in format 1/<n>.
                f.write("};\n")

            f.write("\\\\\n")

        f.write("\\end{tikzpicture}\n")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    midi_pitch_pc_table()
    grid_tatum()