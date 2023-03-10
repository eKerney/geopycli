import typer
from h3Tools import *
from map import foliumMap
from rich import print
from typing import Tuple

app = typer.Typer()

@app.command()
def convert(filename: str = typer.Argument(...), outformat: str = typer.Argument(...), 
            special: str = '', fields: Tuple[str,str] = typer.Option((None,None))):
    """
    Convert from existing GeoData format to specified output format - 
    Outformat options = ['geojson', 'gpkg', 'shapefile', 'flatgeobuf', 'h3', 'filegdb'] - 
    --special options ['h3input', 'gdbinput'] 
    Upper or lowercase
    """
    # print(fields[0])
    geoConvertor(fileName=filename, outFormat=outformat, special=special, fields=fields)

@app.command()
def map(filename: str = typer.Argument(...), zoom: int=12, basemap: str = ''):
    """
    Shoot GeoJSON over to folium Map and open a new browser window
    """
    foliumMap(filename=filename, zoom=zoom, basemap=basemap)
    

if __name__ == "__main__":
    app()
