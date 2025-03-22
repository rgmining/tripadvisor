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
"""Evaluate a review graph mining algorithm with the Trip Advisor dataset.

Usage: python -m tripadvisor [OPTIONS]

  Evaluate a review graph mining algorithm with the Trip Advisor dataset.

Options:
  -m, --method [rsd|feagle|fraudar]
                                  name of algorithm.  [required]
  --loop INTEGER                  number of iteration.
  --threshold FLOAT               threshold.
  --output FILENAME               file path to store results. [Default:
                                  stdout]
  --param TEXT                    key and value a pair of parameters
                                  corresponding to the chosen algorithm,
                                  connected with '='.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
"""

import logging
import sys
from importlib.metadata import version
from typing import TextIO, Callable, Any, Protocol, Final

import click

from tripadvisor.debug import print_state, Graph as PrintableGraph
from tripadvisor.loader import load, Graph as LoadableGraph

LOGGER = logging.getLogger(__name__)


class Graph(PrintableGraph, LoadableGraph, Protocol):
    def update(self) -> float: ...


ALGORITHMS = dict[str, Callable[..., Graph]]()
"""Dictionary of graph loading functions associated with installed algorithms.
"""

# Load and register RIA.
try:
    import ria

    def ignore_args(func: Callable) -> Callable:
        """Returns a wrapped function which ignore given arguments."""

        def _(*_args: tuple[Any]) -> Any:
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

    def create_rsd_graph(**kwargs: float) -> rsd.ReviewGraph:
        """Create a review graph defined in RSD package."""
        if "theta" not in kwargs:
            LOGGER.warning("Parameter 'theta' is not specified. Set to 0.1.")
            kwargs["theta"] = 0.1
        return rsd.ReviewGraph(kwargs["theta"])

    ALGORITHMS["rsd"] = create_rsd_graph
except ImportError:
    LOGGER.info("rgmining-rsd is not installed.")

# Load and register Fraud Eagle.
try:
    import fraud_eagle

    def create_feagle_graph(**kwargs: float) -> fraud_eagle.ReviewGraph:
        """Create a review graph defined in fraud eagle package."""
        if "epsilon" not in kwargs:
            LOGGER.warning("Parameter 'epsilon' is not specified. Set to 0.1.")
            kwargs["epsilon"] = 0.1
        return fraud_eagle.ReviewGraph(kwargs["epsilon"])

    ALGORITHMS["feagle"] = create_feagle_graph
except ImportError:
    LOGGER.info("rgmining-fraud-eagle is not installed.")

# Load and register FRAUDAR.
try:
    import fraudar

    def create_fraudar_graph(**kwargs: float) -> fraudar.ReviewGraph:
        """Create a review graph defined in Fraudar package."""
        if "nblock" not in kwargs:
            LOGGER.warning("Parameter 'nblock' is not specified. Set to 1.")
            kwargs["nblock"] = 1.0
        return fraudar.ReviewGraph(int(kwargs["nblock"]))

    ALGORITHMS["fraudar"] = create_fraudar_graph
except ImportError:
    LOGGER.info("rgmining-fraudar is not installed.")


def run(
    method: str, loop: int, threshold: float, output: TextIO, param: tuple[str]
) -> None:
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
    kwargs = {
        key: float(value) for key, value in [v.split("=") for v in param]
    }

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
@click.option(
    "--param",
    multiple=True,
    help="key and value pair of parameters corresponding to the chosen algorithm, connected with '='.",
)
@click.version_option(version("rgmining-tripadvisor-dataset"))
def main(
    method: str, loop: int, threshold: float, output: TextIO, param: tuple[str]
) -> None:
    """Evaluate a review graph mining algorithm with the Trip Advisor dataset."""
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    run(method, loop, threshold, output, param)


__all__: Final = ["main"]
