import typer
from h3Tools import *
from rich import print

app = typer.Typer()

# concept for format conversions
# gpycli convert --raster --h3 slope.json --(shapefile, geopackage, geojson, csv, zip, h3json)
# gpycli convert slope.geojson (shapefile, geopackage, geojson, csv, zip, h3json, h3csv)

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
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
