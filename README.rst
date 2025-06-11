Trip Advisor Dataset Loader
===========================

|GPLv3| |Build Status| |Release| |PyPi| |Japanese|

|Logo|

For the `Review Graph Mining project <https://github.com/rgmining>`__,
this package provides a loader of the `Trip Advisor
dataset <https://www.cs.virginia.edu/~hw5x/dataset.html>`__ provided by `Dr.
Wang <http://www.cs.virginia.edu/~hw5x/>`__.

Installation
------------

Use pip to install this package.

.. code:: shell

    $ pip install --upgrade rgmining-tripadvisor-dataset

Usage
-----

This package provides module ``tripadvisor`` and this module provides
``load`` function. The ``load`` function takes a graph object.

For example, the following code constructs a graph object provides the
`FRAUDAR <http://www.kdd.org/kdd2016/subtopic/view/fraudar-bounding-graph-fraud-in-the-face-of-camouflage>`__
algorithm, loads the Trip Advisor dataset, runs the algorithm, and then
outputs names of anomalous reviewers. Since this dataset consists of
huge reviews, loading may take long time.

.. code:: py

    import fraudar
    import tripadvisor

    # Construct a graph and load the dataset.
    graph = fraudar.ReviewGraph()
    tripadvisor.load(graph)

    # Run the analyzing algorithm.
    graph.update()

    # Print names of reviewers who are judged as anomalous.
    for r in graph.reviewers:
      if r.anomalous_score == 1:
        print r.name

    # The number of reviewers the dataset has: -> 1169456.
    len(graph.reviewers)

    # The number of reviewers judged as anomalous: -> 147.
    len([r for r in graph.reviewers if r.anomalous_score == 1])

Note that you may need to install the FRAUDAR algorithm for the Review
Mining Project by ``pip install rgmining-fraudar``.

License
-------

This software is released under The GNU General Public License Version
3, see `COPYING <COPYING>`__ for more detail.

The authors of the Trip Advisor dataset, which this software imports,
requires to cite the following papers when you publish research papers
using this package:

-  `Hongning Wang <http://www.cs.virginia.edu/~hw5x/>`__, `Yue
   Lu <https://www.linkedin.com/in/yue-lu-80a6a549>`__, and `ChengXiang
   Zhai <http://czhai.cs.illinois.edu/>`__, "Latent Aspect Rating
   Analysis without Aspect Keyword
   Supervision,"
   In Proc. of the 17th ACM SIGKDD Conference on Knowledge Discovery and
   Data Mining (KDD'2011), pp.618-626, 2011;
-  `Hongning Wang <http://www.cs.virginia.edu/~hw5x/>`__, `Yue
   Lu <https://www.linkedin.com/in/yue-lu-80a6a549>`__, and `Chengxiang
   Zhai <http://czhai.cs.illinois.edu/>`__, "Latent Aspect Rating
   Analysis on Review Text Data: A Rating Regression
   Approach,"
   In Proc. of the 16th ACM SIGKDD Conference on Knowledge Discovery and
   Data Mining (KDD'2010), pp.783-792, 2010.

.. |GPLv3| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://www.gnu.org/copyleft/gpl.html
.. |Build Status| image:: https://github.com/rgmining/tripadvisor/actions/workflows/python-lib.yaml/badge.svg
   :target: https://github.com/rgmining/tripadvisor/actions/workflows/python-lib.yaml
.. |Release| image:: https://img.shields.io/badge/release-0.6.1-brightgreen.svg
   :target: https://github.com/rgmining/tripadvisor/releases/tag/v0.6.1
.. |PyPi| image:: https://img.shields.io/badge/pypi-0.6.1-brightgreen.svg
   :target: https://pypi.python.org/pypi/rgmining-tripadvisor-dataset
.. |Japanese| image:: https://img.shields.io/badge/qiita-%E6%97%A5%E6%9C%AC%E8%AA%9E-brightgreen.svg
   :target: http://qiita.com/jkawamoto/items/86c687d85efb783bcd7d
.. |Logo| image:: https://rgmining.github.io/tripadvisor/_static/image.png
   :target: https://rgmining.github.io/tripadvisor/
