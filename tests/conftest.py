#
# conftest.py
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
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

import pytest


@dataclass(eq=True)
class Reviewer:
    name: str
    anomalous_score: float = 0.0


@dataclass(eq=True)
class Product:
    name: str
    summary: float = 0.0


class Graph:
    reviewers: dict[str, Reviewer]
    products: dict[str, Product]
    reviews: defaultdict[str, dict[str, float]]

    def __init__(self) -> None:
        self.reviewers = dict()
        self.products = dict()
        self.reviews = defaultdict(dict)

    def new_reviewer(self, name: str) -> Reviewer:
        """Create a new reviewer."""
        if name in self.reviewers:
            raise ValueError("The given reviewer already exists:", name)

        r = Reviewer(name)
        self.reviewers[name] = r
        return r

    def new_product(self, name: str) -> Product:
        """Create a new product."""
        if name in self.products:
            raise ValueError("The given product already exists:", name)

        p = Product(name)
        self.products[name] = p
        return p

    def add_review(
        self,
        reviewer: Reviewer,
        product: Product,
        score: float,
        _date: Any | None = None,
    ) -> None:
        """Add a review."""
        if reviewer.name not in self.reviewers:
            raise ValueError("The given reviewer doesn't exist:", reviewer)
        if product.name not in self.products:
            raise ValueError("The given product doesn't exist:", product)
        self.reviews[reviewer.name][product.name] = score


@pytest.fixture
def graph():
    return Graph()
