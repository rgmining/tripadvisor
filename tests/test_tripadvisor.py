#
# test_tripadvisor.py
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
from collections import defaultdict
from typing import Any

import pytest

import tripadvisor


class Graph:
    reviewers: set[str]
    products: set[str]
    reviews: defaultdict[str, dict[str, float]]

    def __init__(self) -> None:
        self.reviewers = set()
        self.products = set()
        self.reviews = defaultdict(dict)

    def new_reviewer(self, name: str) -> str:
        """Create a new reviewer."""
        if name in self.reviewers:
            raise ValueError("The given reviewer already exists:", name)
        self.reviewers.add(name)
        return name

    def new_product(self, name: str) -> str:
        """Create a new product."""
        if name in self.products:
            raise ValueError("The given product already exists:", name)
        self.products.add(name)
        return name

    def add_review(
        self, reviewer: str, product: str, score: float, _date: Any | None = None
    ) -> None:
        """Add a review."""
        if reviewer not in self.reviewers:
            raise ValueError("The given reviewer doesn't exist:", reviewer)
        if product not in self.products:
            raise ValueError("The given product doesn't exist:", product)
        self.reviews[reviewer][product] = score


@pytest.fixture
def graph():
    return Graph()


def test_graph_new_reviewer(graph: Graph) -> None:
    """If create same reviewers, the graph should rises an error."""
    name = "test-reviewer"
    assert graph.new_reviewer(name) == name

    with pytest.raises(ValueError):
        graph.new_reviewer(name)


def test_graph_new_product(graph: Graph) -> None:
    """If create same products, mock should rises an error."""
    name = "test-product"
    assert graph.new_product(name) == name

    with pytest.raises(ValueError):
        graph.new_product(name)


def test_graph_add_review(graph: Graph) -> None:
    """Test add_review method."""
    reviewer = "test-reviewer"
    product = "test-product"

    graph.new_reviewer(reviewer)
    graph.new_product(product)

    score = random.random()
    graph.add_review(reviewer, product, score)
    assert graph.reviews[reviewer][product] == score

    with pytest.raises(ValueError):
        graph.add_review(reviewer, reviewer, score)
    with pytest.raises(ValueError):
        graph.add_review(product, product, score)


def test_load(graph: Graph) -> None:
    """Test load method."""
    assert tripadvisor.load(graph) == graph

    for pmap in graph.reviews.values():
        for score in pmap.values():
            assert 0 <= score <= 1
