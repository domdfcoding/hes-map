========
hes-map
========

.. start short_desc

**Map showing Scotland's historic environment.**

.. end short_desc

.. figure:: https://domdfcoding.github.io/assets/img/hes_map_screenshot.png
   :width: 500px
   :height: 500px
   :alt: Screenshot of the map

   `View The Map`_

-----

| Dataset downloaded from the `Historic Environment Scotland`_.
| Contains Historic Environment Scotland and Ordnance Survey data © Historic Environment Scotland - Scottish Charity No. SC045925 © Crown copyright and database right 2026.
| Licenced under the `Open Government Licence v3 (OGL)`_.

.. _View The map: https://domdfcoding.github.io/hes-map/
.. _Historic Environment Scotland: https://portal.historicenvironment.scot/apex/f?p=PORTAL:downloads:::::DATASET:ALL
.. _Open Government Licence v3 (OGL): https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

-----


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/hes-map/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/hes-map/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/hes-map/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/hes-map/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/hes-map/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/hes-map/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/hes-map/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/hes-map/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/hes-map/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/hes-map/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/hes-map/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/hes-map/
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/hes-map?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/hes-map
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/domdfcoding/hes-map
	:target: https://github.com/domdfcoding/hes-map/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/hes-map
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/hes-map/v0.0.0
	:target: https://github.com/domdfcoding/hes-map/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/hes-map
	:target: https://github.com/domdfcoding/hes-map/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2026
	:alt: Maintenance

.. end shields

Installation
--------------

.. start installation

``hes-map`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/domdfcoding/hes-map

.. end installation
