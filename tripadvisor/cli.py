#
# cli.py
#
# Copyright (c) 2017-2025 Junpei Kawamoto
#
# This file is part of rgmining-tripadvisor-dataset.
#
# rgmining-tripadvisor-dataset is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-tripadvisor-dataset is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Evaluate a review graph mining algorithm with the Trip Advisor dataset."""

import logging
import sys
from typing import TextIO

import click

from tripadvisor import load
from tripadvisor.debug import print_state

LOGGER = logging.getLogger(__name__)

ALGORITHMS = {}
"""Dictionary of graph loading functions associated with installed algorithms.
"""

# Load and register RIA.
try:
    import ria

    def ignore_args(func):
        """Returns a wrapped function which ignore given arguments."""

        def _(*_args):
            """The function body."""
            return func()

        return _

    ALGORITHMS["ria"] = ria.ria_graph
    ALGORITHMS["one"] = ignore_args(ria.one_graph)
    ALGORITHMS["onesum"] = ignore_args(ria.one_sum_graph)
    ALGORITHMS["mra"] = ignore_args(ria.mra_graph)
except ImportError:
    LOGGER.info("rgmining-ria is not installed.")

# Load and register RSD.
try:
    import rsd

    def create_rsd_graph(theta=0.1, **_kwargs):
        return rsd.ReviewGraph(theta)

    ALGORITHMS["rsd"] = create_rsd_graph
except ImportError:
    LOGGER.info("rgmining-rsd is not installed.")

# Load and register Fraud Eagle.
try:
    import fraud_eagle

    def create_feagle_graph(epsilon=0.1, **_kwargs):
        return fraud_eagle.ReviewGraph(epsilon)

    ALGORITHMS["feagle"] = create_feagle_graph
except ImportError:
    LOGGER.info("rgmining-fraud-eagle is not installed.")

# Load and register FRAUDAR.
try:
    import fraudar

    def create_fraudar_graph(nblock=1):
        """Create a review graph defined in Fraudar package."""
        return fraudar.ReviewGraph(int(nblock))

    ALGORITHMS["fraudar"] = create_fraudar_graph
except ImportError:
    LOGGER.info("rgmining-fraudar is not installed.")


def run(method: str, loop: int, threshold: float, output: TextIO, param: tuple[str] = ()):
    """Run a given algorithm with the Trip Advisor dataset.

    Runs a given algorithm and outputs anomalous scores and summaries after
    each iteration finishes. The function will end if a given number of loops
    ends or the update of one iteration becomes smaller than a given threshold.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Argument `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
    argument.

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      threshold: threshold to judge an update is negligible (default: 10^-3).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
    """
    kwargs = {key: float(value) for key, value in [v.split("=") for v in param]}

    graph = ALGORITHMS[method](**kwargs)
    load(graph)

    print_state(graph, 0, output)

    # Updates
    LOGGER.info("Start iterations.")
    for i in range(loop if not method.startswith("one") else 1):
        diff = graph.update()
        if diff is not None and diff < threshold:
            break

        # Current summary
        LOGGER.info("Iteration %d ends. (diff=%s)", i + 1, diff)
        print_state(graph, i + 1, output)

    # Print final state.
    print_state(graph, "final", output)


@click.command()
@click.option(
    "-m",
    "--method",
    type=click.Choice(list(ALGORITHMS.keys()), case_sensitive=False),
    required=True,
    help="name of algorithm.",
)
@click.option("--loop", type=int, default=20, help="number of iteration.")
@click.option("--threshold", type=float, default=10 ^ -3, help="threshold.")
@click.option(
    "--output",
    default=sys.stdout,
    type=click.File("w"),
    help="file path to store results. [Default: stdout]",
)
@click.option("--param", multiple=True, help="key and value pair which are connected with '='.")
def main(method, loop, threshold, output, param) -> None:
    """Evaluate a review graph mining algorithm with the Trip Advisor dataset."""
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    run(method, loop, threshold, output, param)
