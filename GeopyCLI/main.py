import typer
from typer import style
# from geopycliFunctions import geoConvertor
# from map import foliumMap
from rich import print
from typing import Tuple
import pandas as pd
import numpy as np
import shapely
import geopandas as gpd
import math
import h3
import os
import json
from os import error
import folium
import webbrowser

def foliumMap(filename: str, zoom: int, basemap: str):
    # create the empty map
    m = folium.Map(zoom_start=zoom)
    # create the GeoJSON layer to obtain feature properties
    try:
        layer = folium.GeoJson(filename, name='geojson') 
        # Get list of properties from properties.keys() dict
        labels = list(layer.data['features'][0]['properties'].keys())
        # Create tooltip with GeoJSON properties
        tooltip=folium.GeoJsonTooltip(fields=labels, labels=True)
        # add GeoJSON layer to map
        def geoStyle(feature):
            return {
                "fillOpacity": 0.3,
                "weight": 1.0,
                "fillColor": '#851bc2',
                "color": '#3a296e'
        }
        # geoStyle = {'color': '#ff7800', 'weight': 5, 'opacity': 0.65}
        layer = folium.GeoJson(filename,name='geojson',tooltip=tooltip,style_function=geoStyle).add_to(m)
    except KeyError as e:
        print(f'Cannot load layer {filename} - {e}')
    # fit map to layer bounds
    m.fit_bounds(m.get_bounds(), padding=(30, 30))
    m.save('map.html')
    webbrowser.open('map.html')

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
app = typer.Typer()

@app.command()
def convert(filename: str = typer.Argument(...), outformat: str = typer.Argument(...), 
            special: str = '', fields: Tuple[str,str] = typer.Option((None,None))):
    """
    Convert from existing GeoData format to specified output format - 
    Outformat options = ['geojson', 'gpkg', 'shapefile', 'flatgeobuf', 'h3', 'filegdb'] - 
    --special options ['h3input', 'gdbinput'] 
    --fields h3_index axisName (i.e. fields for H3 JSON, first is H3 index, second is score field 
    Upper or lowercase
    """
    geoConvertor(fileName=filename, outFormat=outformat, special=special, fields=fields)

@app.command()
def map(filename: str = typer.Argument(...), zoom: int=12, basemap: str = ''):
    """
    Shoot GeoJSON over to folium Map and open a new browser window
    """
    foliumMap(filename=filename, zoom=zoom, basemap=basemap)
    

if __name__ == "__main__":
    app()
