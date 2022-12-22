# Scans AGOL account for specified feature layer service.
# Returns the layer name and map name within which the service is found.

import arcpy
from arcgis.gis import GIS
from arcgis.mapping import WebMap

# sign into portal
gis = GIS(
    url="https://oriontwp.maps.arcgis.com/",
    username="OHM_Mike",
    password="OHMAdvisors1!",
)


def main():
    print(
        "Logged into {} as {}".format(
            arcpy.GetActivePortalURL(), gis.properties["user"]["username"]
        )
    )

    # the feature layer of interest for which the web maps will be scanned
    service_name = "Abandoned Water Main"
    wm_search(service_name)


# returns the web map title and URL where the input service matches a layer
def wm_search(service_name):
    print(f"searching web maps... ")
    web_maps = gis.content.search(query="", item_type="Web Map", max_items=5000,)
    for item in web_maps:
        web_map = WebMap(item)
        layers = web_map.layers
        for layer in layers:
            try:
                if layer.title == service_name:
                    print(f"{web_map.item.title}")
            except:
                continue
    print("Search Complete")


if __name__ == "__main__":
    main()

