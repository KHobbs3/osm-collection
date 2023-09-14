"""
Script to expand key-value pairs within other_tags column as separate columns.
"""


import pandas as pd
import geopandas as gpd
import sys
import re
import glob

tags = ["building:levels","building:colour","building:flats","building:material",
        "building:max_level","building:min_level","building:part","entrance","height",
        "start_date"]

tags_head = [r'("building:levels"=>".*")',
             r'("building:colour"=>".*")',
             r'("building:flats"=>".*")',
             r'("building:material"=>".*")',
             r'("building:max_level"=>".*")',
             r'("building:min_level"=>".*")',
             r'("building:part"=>".*")',
            r'("entrance"=>".*")',
            r'("height"=>".*")',
            r'("start_date"=>".*")'
            ]


file = sys.argv[1]

# for file in glob.glob("data/*/multipolygons.geojson"):
print(file)

# Read file
df = gpd.read_file(file, driver = "GPKG")

# Clean other_tags column
for key,qry in zip(tags, tags_head):
    # extract keys of interest from other_tags
    temp = df.other_tags\
            .str.extract(qry)[0]\
            .str.split(',', expand = True)[0]

    # if the key is not completely empty, split the key=>value pair and set key as column name, values = values
    if temp.isnull().all() == False:
        df[key] = temp.str.split('=>', expand = True)[1]

    # otherwise, set empty column as the tag field
    else:
        df[key] = temp

fname=re.sub(".gpkg", "", file)
df.head()
df.to_file(f"{fname}-clean.gpkg", driver = "GPKG")
print("done.")