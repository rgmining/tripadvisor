#
# test_loader.py
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
import os

import pytest

import tripadvisor
from tests.conftest import Graph


@pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Skipping this test on CI"
)
def test_load(graph: Graph) -> None:
    """Test load method."""
    assert tripadvisor.load(graph) == graph

    assert len(graph.reviews) > 0
    assert len(graph.products) > 0
    assert len(graph.reviewers) > 0

    for pmap in graph.reviews.values():
        for score in pmap.values():
            assert 0 <= score <= 1
