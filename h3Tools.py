import pandas as pd
import numpy as np
import shapely
import geopandas as gpd
import math
import h3
import os
import json

drivers = {'CSV': 'CSV', 'SHAPEFILE':'ESRI Shapefile', 'FLATGEOBUF':'FlatGeobuf', 'GEOJSON':'GeoJSON', 
        'GPKG': 'GPKG', 'SQLITE':'SQLite', 'TOPOJSON':'TopoJSON', 'GPX':'GPX', 'H3': 'H3', 'FILEGDB':'FileGDB'}

def geoConvertor(fileName: str, outFormat: str, special: str, fields: str):
    outFormat=outFormat.upper()
    print(f'WORKING ON {fileName} to {outFormat}...')
    if special.upper() == 'H3INPUT':
        df = pd.DataFrame(pd.read_json(fileName, typ='series')).reset_index(level=0)
        df = df.set_axis(['h3_index', 'axisName'], axis=1)
        # Initialize dataframe from set of indexes
        df_indexes = gpd.GeoDataFrame(df['h3_index'], columns=['h3_index'])
        # Get coordinate values defining the polygon
        df_indexes['poly_coords'] = df_indexes['h3_index'].apply(lambda x: h3.h3_to_geo_boundary(x))
        # Reverse the order of each x/y point pair - h3 library returns them backwards of how shapely needs them
        df_indexes['poly_coords_good'] = df_indexes['poly_coords'].apply(lambda x: [coord[::-1] for coord in x])
        df_indexes.drop(['poly_coords'], axis=1, inplace=True)
        # Make full hex geometry
        df_indexes['geometry'] = df_indexes['poly_coords_good'].apply(lambda x: shapely.geometry.Polygon(x))
        df_indexes.drop(['poly_coords_good'], axis=1, inplace=True)
        # Make geodataframe in WGS84
        gdf_hexes = gpd.GeoDataFrame(df_indexes, geometry=df_indexes.geometry, crs="EPSG:4326")
        splitNames = fileName.split('.')
        # merge back in data value field from h3 JSON 
        gdf_hexes = gdf_hexes.merge(df, on='h3_index')
        gdf_hexes.reset_index(inplace=True, drop=True)
        gdf_hexes.to_file(f'{splitNames[0]}.{outFormat.lower()}', driver=drivers[outFormat])
    elif special.upper() == 'GDBINPUT':
        gdf = gpd.read_file(fileName, driver='FileGDB',layer=0)
        gdf.to_file(f'{splitNames[0]}.{outFormat.lower()}', driver=drivers[outFormat])
    else:
        splitNames = fileName.split('.')
        if drivers[outFormat] == 'H3':
            gdf = gpd.read_file(fileName).reset_index(drop=True)
            gdf = gdf[[ fields[0], fields[1] ]]
            # gdf = gdf[['h3_index','Score_v4']]
            dataDict = {}
            for row in gdf.itertuples():
                dataDict[row[1]] = float(row[2])
            json_obj = json.dumps(dataDict, indent=1)
            with open(f'{splitNames[0]}.json', 'w') as outfile:
                outfile.write(json_obj)
            print(f'CONVERTED {fileName} TO {splitNames[0]}.json')

        else:
            gdf = gpd.read_file(fileName)
            gdf.to_file(f'{splitNames[0]}.{outFormat.lower()}', driver=drivers[outFormat])
            print(f'CONVERTED {fileName} TO {splitNames[0]}.{outFormat.lower()}')


### index, Score_str
