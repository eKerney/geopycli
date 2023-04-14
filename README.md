# geopy cli
---
A handy command line utility to quickly convert GeoSpatial Data and shoot GeoJSON to a Folium Map.   
### Install
This has been tested on [Linux Ubuntu](https://releases.ubuntu.com/focal/) using Windows Subsystem for Linux. 
Download the Python wheel from the [operations-geoprocess-tools repo](https://github.com/airspace-link-inc/operations-geoprocess-tools/blob/main/dist/GeopyCLI-0.0.1-py3-none-any.whl)
Either install into your root environment to use anywhere, or create new virtual environment:
```bash
python3 -m venv newVirtualEnvironment
source newVirtualEnvironment/bin/activate
pip install GeopyCLI-0.0.1-py3-none-any.whl
```

GeopyCLI is now installed and ready to use!
For help just type:
```bash
GeopyCLI --help
─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ convert  Convert from existing GeoData format to specified output format -  Outformat options = ['geojson', 'gpkg',   │
│          'shapefile', 'flatgeobuf', 'h3', 'filegdb'] -  --special options ['h3input', 'gdbinput']  Upper or lowercase │
│ map      Shoot GeoJSON over to folium Map and open a new browser window                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
You can also get help with either the convert or map command:
```bash
GeopyCLI convert --help 

 Usage: GeopyCLI convert [OPTIONS] FILENAME OUTFORMAT
 
 Convert from existing GeoData format to specified output format -  Outformat options = ['geojson', 'gpkg', 'shapefile',
 'flatgeobuf', 'h3', 'filegdb'] -  --special options ['h3input', 'gdbinput']  Upper or lowercase
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    filename       TEXT  [default: None] [required]                                                                  │
│ *    outformat      TEXT  [default: None] [required]                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --special        TEXT                                                                                                 │
│ --fields         <TEXT TEXT>...  [default: None, None]                                                                │
│ --help                           Show this message and exit.                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### GeopyCLI convert
Convert from GeoJSON to GeoPackage:
```bash
GeopyCLI convert testSurface.geojson gpkg
# output
WORKING ON testSurface.geojson to GPKG...
CONVERTED testSurface.geojson TO testSurface.gpkg
```
 From GeoJSON to Shapefile:
```bash
GeopyCLI convert testSurface.geojson shapefile
# output
WORKING ON testSurface.geojson to SHAPEFILE...
CONVERTED testSurface.geojson TO testSurface.shapefile
```
 From GeoJSON to H3 JSON:
```bash
GeopyCLI convert testSurface.geojson H3 --fields h3_index axisName 
WORKING ON testSurface.geojson to H3...
CONVERTED testSurface.geojson TO testSurface.json
```
Note the --fields flag, here the h3_index field provides an existing h3 index, and axisName is the hex value field.  This is useful for converting a scored GeoJSON Risk Surface into a simple H3 JSON file that is needed for the routing engine.    
From H3 JSON to GeoJSON, use the --special h3input flags to specify H3 JSON input!
```bash
GeopyCLI convert testSurface.json geojson --special h3input        
WORKING ON testSurface.json to GEOJSON...
```
### GeopyCLI map
Show the GeoJSON you just generated in a folium web map:
```bash
GeopyCLI map testSurface.geojson
```
If your WSL browser is not opening correctly, enter this into your bash terminal:
```bash
export BROWSER='/mnt/c/Windows/explorer.exe'
```
You may also want to add that line to your .bashrc file located in your home directory.   

---
Sample map output:
![[map.png|600]]
---
GeopyCLI is written in python, using the [Typer CLI](https://typer.tiangolo.com/typer-cli/) library and rich.  
It utilizes [GeoPandas](https://geopandas.org/en/stable/index.html#) and H3 for the format conversions, and [folium](https://python-visualization.github.io/folium/) to generate maps. 
