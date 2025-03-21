#
# test_graph.py
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
import random

import pytest

from tests.conftest import Graph, Product, Reviewer


def test_graph_new_reviewer(graph: Graph) -> None:
    """If create same reviewers, the graph should rises an error."""
    name = "test-reviewer"

    r = graph.new_reviewer(name)
    assert r.name == name

    with pytest.raises(ValueError):
        graph.new_reviewer(name)


def test_graph_new_product(graph: Graph) -> None:
    """If create same products, mock should rises an error."""
    name = "test-product"

    p = graph.new_product(name)
    assert p.name == name

    with pytest.raises(ValueError):
        graph.new_product(name)


def test_graph_add_review(graph: Graph) -> None:
    """Test add_review method."""
    reviewer = graph.new_reviewer("test-reviewer")
    product = graph.new_product("test-product")

    score = random.random()
    graph.add_review(reviewer, product, score)
    assert graph.reviews[reviewer.name][product.name] == score

    with pytest.raises(ValueError):
        graph.add_review(reviewer, Product("missing product"), score)
    with pytest.raises(ValueError):
        graph.add_review(Reviewer("missing reviewer"), product, score)
