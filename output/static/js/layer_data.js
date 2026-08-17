var battlefieldsIcon = L.ExtraMarkers.icon(
	{"innerHTML": "<img src='static/img/Challenge_Icon.svg' style='margin: 8px'>", "markerColor": "orange"}
);

var listedBuildingsIcon = L.ExtraMarkers.icon(
	{"icon": "fa-building", "markerColor": "#006fb2", "prefix": "fa", "svg": true}
);

var gardensLandscapesIcon = L.ExtraMarkers.icon(
	{"icon": "fa-tree", "markerColor": "green", "prefix": "fa", "svg": false}
);

var marineProtectedAreasIcon = L.ExtraMarkers.icon(
	{"icon": "fa-anchor", "markerColor": "purple", "prefix": "fa", "svg": true}
);

var scheduledMonumentsIcon = L.ExtraMarkers.icon(
	{"icon": "fa-monument", "markerColor": "#a32d2f", "prefix": "fa", "svg": true}
);

var worldHeritageSitesIcon = L.ExtraMarkers.icon(
	{"icon": "fa-certificate", "markerColor": "grey", "prefix": "fa", "svg": true}
);


const layerData = [
    {
        "variable_prefix": "battlefields",
        "layer": "marker_cluster_battlefields",
        "icon": battlefieldsIcon,
        "noun": "Battlefield",
    },
    {
        "variable_prefix": "listedBuildings",
        "layer": "marker_cluster_listed_buildings",
        "icon": listedBuildingsIcon,
        "noun": "Listed Building",
    },
    {
        "variable_prefix": "gardensLandscapes",
        "layer": "marker_cluster_gardens_landscapes",
        "icon": gardensLandscapesIcon,
        "noun": "Garden and Designed Landscape",
    },
    {
        "variable_prefix": "marineProtectedAreas",
        "layer": "marker_cluster_marine_protected_areas",
        "icon": marineProtectedAreasIcon,
        "noun": "Historic Marine Protected Area",
    },
    {
        "variable_prefix": "scheduledMonuments",
        "layer": "marker_cluster_scheduled_monuments",
        "icon": scheduledMonumentsIcon,
        "noun": "Scheduled Monument",
    },
    {
        "variable_prefix": "worldHeritageSites",
        "layer": "marker_cluster_world_heritage_sites",
        "icon": worldHeritageSitesIcon,
        "noun": "World Heritage Site",
    },
]
