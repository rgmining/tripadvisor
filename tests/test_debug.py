#
# test_debug.py
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
import io

from tests.conftest import Graph
from tripadvisor.debug import print_state


def test_print_state(graph: Graph) -> None:
    # Create reviewers and products.
    reviewers = [graph.new_reviewer(f"reviewer-{i}") for i in range(1, 4)]
    products = [graph.new_product(f"product-{i}") for i in range(1, 3)]

    # Add reviews.
    graph.add_review(reviewers[0], products[0], 0.3)
    graph.add_review(reviewers[0], products[1], 0.9)
    graph.add_review(reviewers[1], products[1], 0.1)
    graph.add_review(reviewers[2], products[1], 0.5)

    count = 9

    output = io.StringIO()
    print_state(graph, count, output)

    assert (
        output.getvalue()
        == """{"iteration": 9, "reviewer": {"reviewer_id": "reviewer-1", "score": 0.0}}
{"iteration": 9, "reviewer": {"reviewer_id": "reviewer-2", "score": 0.0}}
{"iteration": 9, "reviewer": {"reviewer_id": "reviewer-3", "score": 0.0}}
{"iteration": 9, "product": {"product_id": "product-1", "summary": 0.0}}
{"iteration": 9, "product": {"product_id": "product-2", "summary": 0.0}}
"""
    )
