#!/usr/bin/env python3
#
#  constants.py
"""
String constants.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
from nhle_map.constants import Dataset
from nhle_map.icons import FontawesomeLayerIcon, SVGLayerIcon

__all__ = [
		"BATTLEFIELDS",
		"LAYERS",
		"LISTED_BUILDINGS",
		"MARINE_PROTECTED_AREAS",
		"MAX_LAT",
		"MAX_LNG",
		"MIN_LAT",
		"MIN_LNG",
		"PARKS_AND_GARDENS",
		"SCHEDULED_MONUMENTS",
		"WORLD_HERITAGE_SITES",
		]

BATTLEFIELDS = Dataset(
		variable_prefix="battlefields",
		identifier="battlefields",
		name="Battlefields",
		noun="Battlefield",
		icon=SVGLayerIcon(filename="static/img/Challenge_Icon.svg", marker_colour="orange"),
		geojson_filename="Battlefields.geojson",
		polygonal=True,
		)

LISTED_BUILDINGS = Dataset(
		variable_prefix="listedBuildings",
		identifier="listed_buildings",
		name="Listed Buildings",
		noun="Listed Building",
		icon=FontawesomeLayerIcon(icon="building", marker_colour="#006fb2", svg_marker=True),
		geojson_filename="Listed Building points.geojson",
		# polygons_geojson_filename="Listed Building polygons.geojson",
		# hidden_polygons=True,
		)

PARKS_AND_GARDENS = Dataset(
		variable_prefix="gardensLandscapes",
		identifier="gardens_landscapes",
		name="Gardens and Designed Landscapes",
		noun="Garden and Designed Landscape",
		icon=FontawesomeLayerIcon(icon="tree", marker_colour="green"),
		geojson_filename="Gardens and Designed Landscapes.geojson",
		polygonal=True,
		)

MARINE_PROTECTED_AREAS = Dataset(
		variable_prefix="marineProtectedAreas",
		identifier="marine_protected_areas",
		name="Historic Marine Protected Areas",
		noun="Historic Marine Protected Area",
		icon=FontawesomeLayerIcon(icon="anchor", marker_colour="purple", svg_marker=True),
		geojson_filename="Marine Protected Areas.geojson",
		# polygonal=True,
		)

SCHEDULED_MONUMENTS = Dataset(
		variable_prefix="scheduledMonuments",
		identifier="scheduled_monuments",
		name="Scheduled Monuments",
		noun="Scheduled Monument",
		icon=FontawesomeLayerIcon(icon="monument", marker_colour="#a32d2f", svg_marker=True),
		geojson_filename="Scheduled Monuments.geojson",
		polygonal=True,
		)

WORLD_HERITAGE_SITES = Dataset(
		variable_prefix="worldHeritageSites",
		identifier="world_heritage_sites",
		name="World Heritage Sites",
		noun="World Heritage Site",
		icon=FontawesomeLayerIcon(icon="certificate", marker_colour="grey", svg_marker=True),
		geojson_filename="World Heritage Sites.geojson",
		polygonal=True,
		)

LAYERS = [
		BATTLEFIELDS,
		LISTED_BUILDINGS,
		PARKS_AND_GARDENS,
		MARINE_PROTECTED_AREAS,
		SCHEDULED_MONUMENTS,
		WORLD_HERITAGE_SITES,
		]

MIN_LAT = 54
MIN_LNG = -8
MAX_LAT = 61
MAX_LNG = 1
