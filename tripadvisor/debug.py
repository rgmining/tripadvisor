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
import json
import sys


def print_state(g, i, output=sys.stdout):
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
                "reviewer": {"reviewer_id": r.name, "score": r.anomalous_score},
            },
            output,
        )
        output.write("\n")

    for p in g.products:
        json.dump(
            {
                "iteration": i,
                "product": {"product_id": p.name, "summary": float(str(p.summary))},
            },
            output,
        )
        output.write("\n")
