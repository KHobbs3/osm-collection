"""
Script to explore osm data sparsity and tag frequency.
"""

import geopandas as gpd
import missingno as msno
import pandas as pd
import plotly.express as px
import re
import glob

temp_gdf = []
for file in glob.glob("data/*/multipolygons-clean.*"):
    fname = re.split("/", file)[1]
    print(fname)

    temp = gpd.read_file(file)
    temp['Prov/Terr'] = fname

    temp_gdf.append(temp)

osm = pd.concat(temp_gdf)

cols = ['name', 'amenity', 'boundary', 'building', 'historic', 'land_area',
       'landuse', 'leisure', 'building:levels',
       'building:colour', 'building:flats', 'building:material',
       'building:max_level', 'building:min_level', 'building:part', 'entrance',
       'height', 'start_date', 'geometry', 'Prov/Terr']

# osm.reset_index().groupby('building').nunique()['index'].reset_index().to_csv("analysis/building_type_counts.csv", index = False)
# osm.reset_index().groupby(['Prov/Terr', 'building']).nunique()['index'].reset_index().to_csv("analysis/PT_building_type_counts.csv", index = False)

# fig = msno.bar(osm[cols])
# fig_copy = fig.get_figure()
# fig_copy.savefig('msno_bar.png', bbox_inches = 'tight')


data = osm.reset_index().groupby(['Prov/Terr', 'building']).count()['index'].reset_index().pivot(
    index = 'Prov/Terr',
    columns = 'building',
    values = 'index'
)

fig2 = px.imshow(data,
                width=800,
                height=500,
                color_continuous_scale = px.colors.sequential.Darkmint,
                title = "Count of building tags by Prov/Terr")

# fig2_copy = fig2.get_figure()
fig2.savefig('analysis/heatmap.png', bbox_inches = 'tight')
