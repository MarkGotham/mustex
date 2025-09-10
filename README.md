# mustex

This `mustex` library is for 
using Python to generate
music-related figures in 
LaTex.

Use `mustex` to make musical-tex figures, and avoiding mus-takes ;)


## Why bother?

LaTex allows for the creation of items programmatically, so why bother involving an external language?

Two reasons.
1. More people are fluent in python than (at least this corner of) LaTex 
2. We will often want figures that are 
broadly consistent, but with 
one-off adjustments to individual elements.
In such contexts, it's worth separating 
the programmatic creation of the figure (here)
from the fine-tuning (in LaTex).

The programmatic side here ensures consistency and
creates deliberately verbose figures with every node spelt out.
That verbose result can be tailored freely, node by node in LaTex.


## Diagram Types

So far this repo covers diagrams for:
- Schema with structured elements and arrows.
- Cycles (single and double), e.g., for pitch and beat class diagrams.
- Linear tables: tabular comparison and grid/tatum.


## Licence

MIT