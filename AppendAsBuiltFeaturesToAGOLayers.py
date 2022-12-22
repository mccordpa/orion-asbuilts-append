# Appends the edits from an as built to the appropriate AGO master layer.
# This step is part of the new workflow (as of November 2022) that will be used to apply as built edits to Orion's GIS since the Orion SDE is no longer used as the master source. It is now AGO.
# *NOTE: In order for this script to append the edits to the correct layer, the name of the as built GDB layer within the Pro doc's Table of Contents
# *must match the the name of the feature layer within the data source of the AGO layer.
# *For example, the following would be a match for Hydrants where the as built GDB layer in the ToC is named Water_Hydrants and the data source of the AGO layer
# *is: https://services3.arcgis.com/gyfj2L6R5jrBGa0s/arcgis/rest/services/Water_Hydrants/FeatureServer
# *As a result, there is a little bit of prepping that is needed to make sure the matches happen. Therefore, the prepping needs to be done on the names of the
# *GDB as built layers within the ToC of the Pro doc.
#!!!BE AWARE: There may be instances where the name of the GDB layer within the ToC might be entirely contained within the data source name of the Feature Layer.
#!!!An example of this is Water Main. If the as built GDB Water Main layer is called wMain in the ToC and the data source for the Stormwater Main AGO layer is called
#!!!swMain, then the below script will try to pair the two layers since 'wMain' is included within 'swMain'.

import arcpy

# Set up Pro document
aprx = arcpy.mp.ArcGISProject("CURRENT")
mp = aprx.listMaps()[0]
all_layers = mp.listLayers()

# Isolate all GDB as built layers together into their own list
# NOTE: The below data source will change dependent on the project
gdb_data_source = "H:\GIS\Working\McCord\Orion\EsysConsolidation\EsysConsolidation_AsBuilt\EsysConsolidation.gdb"
as_built_layers = []
for lyr in all_layers:
    if lyr.supports("DATASOURCE"):
        if gdb_data_source in lyr.dataSource:
            as_built_layers.append(lyr)

# Isolate all AGO layers together into their own list
# NOTE: The below data source will change dependent on the project
ago_data_source = "https://services3.arcgis.com/gyfj2L6R5jrBGa0s/arcgis/rest/services"
ago_layers = []
for lyr in all_layers:
    if lyr.supports("DATASOURCE"):
        if ago_data_source in lyr.dataSource:
            ago_layers.append(lyr)

# iterate through the list of as built GDB layers and AGO layers to find a match between the
# name of the GDB as built layer within the Pro doc's ToC and the name of the AGO Feature Layer
# within its data source
for gdb_lyr in as_built_layers:
    print(f"**** {gdb_lyr.name}****")
    for ago_lyr in ago_layers:
        # TODO: REFINE THE BELOW IF STATEMENT SO THAT ONLY EXACT STRING MATCHES RESULT IN A PAIRING
        if gdb_lyr.name in ago_lyr.dataSource:
            print(f"Appending {gdb_lyr.name} to {ago_lyr.name}")
            arcpy.management.Append(gdb_lyr, ago_lyr, "TEST")

print("Script Complete")
