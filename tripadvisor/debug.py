#
# debug.py
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
"""This module provides a debug function for the Trip Advisor Dataset."""

import json
import sys
from typing import Protocol, TextIO, Any, TypeVar


class Reviewer(Protocol):
    """A protocol for a reviewer object."""

    @property
    def name(self) -> str:
        """The reviewer's ID.'"""

    @property
    def anomalous_score(self) -> float:
        """The anomalous score of the reviewer."""


class Product(Protocol):
    """A protocol for a product object."""

    @property
    def name(self) -> str:
        """The product's ID.'"""

    @property
    def summary(self) -> Any:
        """The summary of the reviews for the product."""


RT = TypeVar("RT", bound=Reviewer)
PT = TypeVar("PT", bound=Product)


class Graph(Protocol[RT, PT]):
    """A protocol for a graph object."""

    @property
    def reviewers(self) -> list[RT]:
        """A list of reviewers."""

    @property
    def products(self) -> list[PT]:
        """A list of products."""


def print_state(g: Graph, i: int | str, output: TextIO = sys.stdout) -> None:
    """Print a current state of a given graph.

    This method outputs a current of a graph as a set of json objects.
    Graph objects must have two properties, `reviewers` and `products`.
    Those properties return a set of reviewers and products respectively.
    See the :ref:`graph interface <dataset-io:graph-interface>`
    for more information.

    In this output format, each line represents a reviewer or product object.

    Reviewer objects are defined as ::

        {
           "iteration": <the iteration number given as i>
           "reviewer":
           {
              "reviewer_id": <Reviewer's ID>
              "score": <Anomalous score of the reviewer>
           }
        }

    Product objects are defined as ::

        {
           "iteration": <the iteration number given as i>
           "reviewer":
           {
              "product_id": <Product's ID>
              "summary": <Summary of the reviews for the product>
           }
        }

    Args:
      g: Graph instance.
      i: Iteration number.
      output: A writable object (default: sys.stdout).
    """
    for r in g.reviewers:
        json.dump(
            {
                "iteration": i,
                "reviewer": {
                    "reviewer_id": r.name,
                    "score": r.anomalous_score,
                },
            },
            output,
        )
        output.write("\n")

    for p in g.products:
        json.dump(
            {
                "iteration": i,
                "product": {
                    "product_id": p.name,
                    "summary": float(str(p.summary)),
                },
            },
            output,
        )
        output.write("\n")
