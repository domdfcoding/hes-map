#!/usr/bin/env python3
#
#  data.py
"""
Data preparation.
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

# stdlib
import datetime
from typing import Any, NamedTuple

# 3rd party
import requests
import shapefile
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from pyproj import CRS, Transformer

# this package
from hes_map import constants

__all__ = ["download_data"]

input_projection = CRS("epsg:27700")
output_projection = CRS("epsg:4326")
transform = Transformer.from_crs(input_projection, output_projection).transform


class Shapefile(NamedTuple):
	download_url: str
	shp_filename: str
	polygons_filename: str | None = None


SHAPEFILES = {
		constants.BATTLEFIELDS.identifier:
				Shapefile(
						"https://inspire.hes.scot/AtomService/DATA/battlefields_scotland.zip",
						"Battlefields_Inventory_Boundary.shp",
						),
		constants.LISTED_BUILDINGS.identifier:
				Shapefile(
						"https://inspire.hes.scot/AtomService/DATA/lb_scotland.zip",
						"Listed_Buildings.shp",
						"Listed_Buildings_boundaries.shp",
						),
		constants.PARKS_AND_GARDENS.identifier:
				Shapefile(
						"https://inspire.hes.scot/AtomService/DATA/gdl_scotland.zip",
						"Gardens_and_Designed_Landscapes.shp",
						),
		constants.MARINE_PROTECTED_AREAS.identifier:
				Shapefile(
						"https://inspire.hes.scot/AtomService/DATA/HMPA_scotland.zip",
						"Historic_Marine_Protected_Areas.shp",
						),
		constants.SCHEDULED_MONUMENTS.identifier:
				Shapefile("https://inspire.hes.scot/AtomService/DATA/sam_scotland.zip", "Scheduled_Monuments.shp"),
		constants.WORLD_HERITAGE_SITES.identifier:
				Shapefile("https://inspire.hes.scot/AtomService/DATA/WHS.zip", "World_Heritage_Sites.shp"),
		}


def download_data(output_directory: PathLike) -> dict[str, Any]:
	"""
	Download data from ``data.gouv.fr``.

	:param output_directory: Directory to write files to.
	"""

	output_dir = PathPlus(output_directory)
	output_dir.maybe_make(parents=True)

	meta: dict[str, Any] = {
			"start_time": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
			"layers": [],
			}

	for layer in constants.LAYERS:
		download_url = SHAPEFILES[layer.identifier].download_url
		resp = requests.get(download_url)
		zip_filename = output_dir / f"{layer.identifier}.zip"
		zip_filename.write_bytes(resp.content)
		sf = shapefile.Reader((zip_filename / SHAPEFILES[layer.identifier].shp_filename).as_posix())
		created_at = datetime.datetime.now()  # TODO

		# TODO: get description from e.g. https://inspire.hes.scot/arcgis/services/HES/World_Heritage_Sites/MapServer/WFSServer?request=GetCapabilities&service=WFS
		meta["layers"].append({
				"name": layer.geojson_filename_stem,
				"description": '',
				"copyrightText": '',  # TODO
				"editingInfo": {
						"dataLastEditDate": created_at.timestamp() * 1000,
						"lastEditDate": created_at.timestamp() * 1000,
						},
				})

		records = sf.records()
		total_lines = len(records)

		geojson = {
				"type": "FeatureCollection",
				"features": [],
				"totalFeatures": total_lines,
				"numberMatched": total_lines,
				"numberReturned": total_lines,
				"timeStamp": created_at.isoformat(),
				"crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}},
				}

		for record in records:
			feature = record.as_dict()

			# TODO: use SHAPE for polygons
			if "LON" in feature:
				lat, lng = feature["LAT"], feature["LON"]
			else:
				lat, lng = transform(feature['X'], feature['Y'])

			if feature["DES_TYPE"] == "WORLD HERITAGE SITE":
				feature["DES_TYPE"] = feature["DES_TYPE"].title()

			assert feature["DES_TYPE"] == layer.noun, (feature["DES_TYPE"], layer.noun)

			list_date = datetime.datetime.combine(
					feature.get("DESIGNATED", feature["CREATED"]),
					datetime.time.min,
					).timestamp() * 1000
			feature_properties = {
					"Grade": feature.get("CATEGORY"),
					"Name": feature["DES_TITLE"],  # or ENT_TITLE?
					"ListDate": list_date,
					"hyperlink": feature["LINK"],
					"ListEntry": feature["DES_REF"],
					}
			geojson["features"].append({
					"type": "Feature",
					"id": feature_properties["ListEntry"],
					"geometry": {"type": "MultiPoint", "coordinates": [[lng, lat]]},
					"geometry_name": "geom",
					"properties": feature_properties,
					})

			# TODO: other relevant properties e.g. CLASS, GROUPCAT, NAT_PARK, AMENDED
			# TODO: notes, poly

		(output_dir / layer.geojson_filename).dump_json(geojson)

	output_dir.joinpath("meta.json").dump_json(meta, indent=2)
	return meta
