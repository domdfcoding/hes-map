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
import re
import xml.etree.ElementTree
import zipfile
from typing import Any, NamedTuple, TypedDict
from xml.etree.ElementPath import findtext

# 3rd party
import pycrs  # type: ignore[import-untyped]
import requests
import shapefile  # type: ignore[import-untyped]
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

	atom_data = parse_atom_data()

	for layer in constants.LAYERS:
		download_url = SHAPEFILES[layer.identifier].download_url
		resp = requests.get(download_url)
		zip_filename = output_dir / f"{layer.identifier}.zip"
		zip_filename.write_bytes(resp.content)
		sf = shapefile.Reader((zip_filename / SHAPEFILES[layer.identifier].shp_filename).as_posix())

		with zipfile.ZipFile(zip_filename, 'r') as archive:
			wkt = archive.read(SHAPEFILES[layer.identifier].shp_filename.replace(".shp", ".prj"))
			crs = pycrs.parse.from_esri_wkt(wkt.decode("UTF-8")).name

		layer_atom_data: AtomData = atom_data.get(
				layer.name,
				{"title": '', "summary": '', "updated": datetime.datetime.now()},
				)
		description = layer_atom_data["summary"]
		created_at = layer_atom_data["updated"]
		meta["layers"].append({
				"name": layer.geojson_filename_stem,
				"description": description,
				"copyrightText": '',  # TODO
				"editingInfo": {
						"dataLastEditDate": created_at.timestamp() * 1000,
						"lastEditDate": created_at.timestamp() * 1000,
						},
				})

		records = sf.shapeRecords()
		total_lines = len(records)

		geojson: GeoJSON = {
				"type": "FeatureCollection",
				"features": [],
				"totalFeatures": total_lines,
				"numberMatched": total_lines,
				"numberReturned": total_lines,
				"timeStamp": created_at.isoformat(),
				"crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}},
				}

		for shaperecord in records:
			feature = shaperecord.record.as_dict()
			shape = shaperecord.shape

			if feature["DES_TYPE"] == "WORLD HERITAGE SITE":
				feature["DES_TYPE"] = feature["DES_TYPE"].title()
				if "buffer zone" in feature["DES_TITLE"].lower():
					continue
				else:
					feature["DES_TITLE"] = feature["DES_TITLE"].replace(" World Heritage Site Boundary", '')
					# TODO: clean up polygon for the Antonine Wall, Orkney and Flow Country - all multipolygons
			elif feature["DES_TYPE"] == "Historic Marine Protected Area":
				feature["DES_TITLE"] = feature["DES_TITLE"].replace("Historic Mpa", '')
				feature["DES_TITLE"] = feature["DES_TITLE"].replace(" Mpa", '')
				# TODO: merge multiple entries with same ID together as multipolygon. Might be needed for some other types too

			assert feature["DES_TYPE"] == layer.noun, (feature["DES_TYPE"], layer.noun)

			list_date = datetime.datetime.combine(
					feature.get("DESIGNATED", feature["CREATED"]),
					datetime.time.min,
					).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
			feature_properties = {
					"Grade": feature.get("CATEGORY"),
					"Name": feature["DES_TITLE"],  # or ENT_TITLE?
					"ListDate": list_date,
					"hyperlink": feature["LINK"],
					"ListEntry": feature["DES_REF"],
					}

			if layer.polygonal:
				assert shape.shapeTypeName == "POLYGON"

				assert len(shape.points)
				if crs == "GCS_WGS_1984":
					polygon = [(lng, lat) for (lng, lat) in shape.points]
				else:
					# TODO: flip lat lng and not output
					polygon = [transform(lat, lng)[::-1] for (lat, lng) in shape.points]

				polygon.append(polygon[0])

				geojson["features"].append({
						"type": "Feature",
						"id": feature_properties["ListEntry"],
						"geometry": {"type": "Polygon", "coordinates": [polygon]},
						"geometry_name": "geom",
						"properties": feature_properties,
						})

			else:
				if "LON" in feature:
					assert crs == "GCS_WGS_1984"
					lat, lng = feature["LAT"], feature["LON"]
				elif crs == "GCS_WGS_1984":
					lat, lng = feature['X'], feature['Y']
				else:
					lat, lng = transform(feature['X'], feature['Y'])

				geojson["features"].append({
						"type": "Feature",
						"id": feature_properties["ListEntry"],
						"geometry": {"type": "MultiPoint", "coordinates": [[lng, lat]]},
						"geometry_name": "geom",
						"properties": feature_properties,
						})

			# TODO: other relevant properties e.g. CLASS, GROUPCAT, NAT_PARK, AMENDED
			# TODO: notes, poly

		assert layer.geojson_filename is not None
		(output_dir / layer.geojson_filename).dump_json(geojson)

	output_dir.joinpath("meta.json").dump_json(meta, indent=2)
	return meta


class GeoJSON(TypedDict):
	type: str
	features: list[dict[str, Any]]
	totalFeatures: int
	numberMatched: int
	numberReturned: int
	timeStamp: str
	crs: dict[str, Any]


def _process_atom_title(title: str) -> str:
	title = title.replace("Historic Environment Scotland - ", '')
	title = title.replace(" (INSPIRE pre-defined download service)", '')
	title = title.replace(" Inventory Boundary", '')
	return title.strip()


def _process_atom_summary(summary: str) -> str:
	summary = summary.split("Shapefile file download")[0]
	summary = re.sub("<!--(.*)-->", '', summary, flags=re.DOTALL)
	summary = summary.replace("<div>", '')
	summary = summary.replace("</div>", '')
	summary = re.sub("\n\\s+", '\n', summary, flags=re.DOTALL)
	summary = summary.replace("<div><br/><div>", '')
	summary = summary.replace('â', '"')
	summary = summary.replace("", '')
	summary = summary.replace("", '')
	summary = summary.rstrip().removesuffix("<br/>")
	return summary.strip()


_ATOM_NS = "{http://www.w3.org/2005/Atom}"


class AtomData(TypedDict):
	title: str
	updated: datetime.datetime
	summary: str


def parse_atom_data() -> dict[str, AtomData]:  # TODO: TypedDict
	resp = requests.get("https://inspire.hes.scot/AtomService/HES_AtomService.atom.en.xml")
	resp.raise_for_status()
	root = xml.etree.ElementTree.fromstring(resp.text)

	data: list[AtomData] = []

	for entry in root.iter(_ATOM_NS + "entry"):
		title = _process_atom_title(findtext(entry, _ATOM_NS + "title", ''))
		updated_isoformat = findtext(entry, _ATOM_NS + "updated", '') or "1970-01-01"
		updated = datetime.datetime.fromisoformat(updated_isoformat + "T00:00+00:00")
		summary = _process_atom_summary(findtext(entry, _ATOM_NS + "summary", ''))
		data.append({
				"title": title,
				"updated": updated,
				"summary": summary,
				})

	return {e["title"]: e for e in data}
