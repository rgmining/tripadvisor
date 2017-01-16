#
# tripadvisor.py
#
# Copyright (c) 2017 Junpei Kawamoto
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
from __future__ import division
import glob
import json


def load(g):
    """Load the Trip Advisor dataset.

    Args:
      g: an instance of bipartite graph.

    Returns:
      The graph instance *g*.
    """
    R = {}  # Reviewers dict.
    for path in glob.iglob("data/*.json"):

        with open(path) as fp:
            obj = json.load(fp)

            target = obj["HotelInfo"]["HotelID"]
            product = g.new_product(name=target)

            for r in obj["Reviews"]:
                name = r["ReviewID"]
                score = float(r["Ratings"]["Overall"]) / 5.

                if name not in R:
                    R[name] = g.new_reviewer(name=name)
                g.add_review(R[name], product, score)

    return g
