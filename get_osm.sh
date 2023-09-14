#!/bin/bash

"""
Script to:
    1. Download data from Geofabrik by province/territory
    2. Extract and convert data to geojson/geopackage
    3. Clean the other_tags column and expand key:values to be distinct columns
"""

cd data/

declare -a StringArray=(
                        "manitoba" 
                        "british-columbia" 
                        "alberta" 
                        "saskatchewan" 
                        "ontario" 
                        "quebec" 
                        "newfoundland-and-labrador" 
                        "nova-scotia" 
                        "new-brunswick" 
                        "prince-edward-island" 
                        "yukon" 
                        "nunavut"
                        "northwest-territories"
                        )


# download and extract osm data
for value in ${StringArray[@]}; 
do

    echo $value
    mkdir $value
    cd $value
   
    wget https://download.geofabrik.de/north-america/canada/${value}-latest.osm.pbf
#     bzip2 -d ${value}-latest.osm.bz2
#     rm -rf ${value}-latest.osm.bz2
    ogr2ogr -f GPKG multipolygons.gpkg ${value}-latest.osm.pbf multipolygons
    rm -rf ${value}-latest.osm.pbf

    # read osm data and clean building tags
    python read_osm.py data/$value/multipolygons.gpkg

    # delete downloads to save memory
    rm -f ${value}-latest.osm
    
    cd ../
done
