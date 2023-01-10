import typer
from h3Tools import *
from map import foliumMap
from rich import print

app = typer.Typer()

@app.command()
def printStuff(info: str = typer.Argument(...)):
    data = {
    "name": "Rick",
    "age": 42,
    "items": [{"name": "Portal Gun"}, {"name": "Plumbus"}],
    "active": True,
    "affiliation": None,
    }
    print(f'Testing print with rich {data}')
    print(data)

@app.command()
def convert(filename: str = typer.Argument(...), outformat: str = typer.Argument(...), 
            raster: bool = False, h3input: bool = False):
    """
    Convert from existing GeoData format to specified output format
    outformat options = ['geojson', 'gpkg', 'shapefile', 'csv', 'gpx', 'flatgeobuf', 'topojson']
    Upper or lowercase
    """
    geoConvertor(fileName=filename, outFormat=outformat, raster=raster, h3Input=h3)

@app.command()
def map(filename: str = typer.Argument(...), zoom: int=12, basemap: str = ''):
    foliumMap(filename=filename, zoom=zoom, basemap=basemap)

if __name__ == "__main__":
    app()
