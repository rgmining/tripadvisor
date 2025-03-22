#
# loader.py
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
"""This module provides a function to load the Trip Advisor dataset."""

import json
import logging
import tarfile
from collections.abc import Iterator
from contextlib import closing
from datetime import datetime
from typing import Any, BinaryIO, cast, Protocol, TypeVar

import requests
from platformdirs import user_cache_path
from tqdm import tqdm

LOGGER = logging.getLogger(__name__)

DATASET_URL = "https://www.cs.virginia.edu/~hw5x/Data/LARA/TripAdvisor/TripAdvisorJson.tar.bz2"
FILENAME = "TripAdvisorJson.tar.bz2"

_DATE_FORMAT = "%B %d, %Y"
"""Data format in the dataset.
"""

RT = TypeVar("RT")
PT = TypeVar("PT")


class Graph(Protocol[RT, PT]):
    """A protocol class representing a graph object.

    This protocol defines the methods required for a class to be used
    as the graph object in the `load` function. The graph object facilitates
    creating reviewers, products, and adding reviews.
    """

    def new_reviewer(
        self, name: str, anomalous_score: float | None = None
    ) -> RT:
        """Creates a new reviewer node in the graph.

        Args:
            name: The name of the reviewer.
            anomalous_score: Optional. The initial anomalous score for the reviewer.

        Returns:
            The created reviewer node.
        """

    def new_product(self, name: str) -> PT:
        """Creates a new product node in the graph.

        Args:
            name: The name of the product.

        Returns:
            The created product node.
        """

    def add_review(
        self, reviewer: RT, product: PT, score: float, time: int | None = None
    ) -> Any:
        """Adds a review connecting a reviewer to a product with a score and time.

        Args:
            reviewer: The reviewer node.
            product: The product node.
            score: The score of the review.
            time: Optional. The time of the review.
        """


def reviews() -> Iterator[dict[str, Any]]:
    """Load the Trip Advisor dataset."""

    data_path = user_cache_path(
        "rgmining-tripadvisor-dataset", ensure_exists=True
    ).joinpath(FILENAME)
    if not data_path.exists():
        LOGGER.info(
            "Not found review data locally, downloading them from %s...",
            DATASET_URL,
        )

        res = requests.get(DATASET_URL, stream=True)
        res.raise_for_status()
        with open(data_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=32 * 1024):
                f.write(chunk)

        LOGGER.info("Downloaded review data are stored at %s", data_path)

    with tarfile.open(data_path) as tar:
        LOGGER.info("Extracting review data from %s...", data_path)
        for info in tqdm(tar.getmembers()):
            if not info.isfile():
                continue

            with closing(cast(BinaryIO, tar.extractfile(info))) as fp:
                yield json.load(fp)
                return


def load(graph: Graph) -> Graph:
    """Load the Trip Advisor dataset to a given graph object.

    Args:
      graph: an instance of review graph.

    Returns:
      The graph instance *graph*.
    """
    R = {}  # Reviewers dict.
    for obj in reviews():
        target = obj["HotelInfo"]["HotelID"]
        product = graph.new_product(name=target)

        for r in obj["Reviews"]:
            name = r["ReviewID"]
            score = float(r["Ratings"]["Overall"]) / 5.0

            try:
                date = int(
                    datetime.strptime(r["Date"], _DATE_FORMAT).strftime(
                        "%Y%m%d"
                    )
                )
            except ValueError:
                date = None

            if name not in R:
                R[name] = graph.new_reviewer(name=name)
            graph.add_review(R[name], product, score, date)

    return graph
