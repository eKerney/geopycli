# geopy cli
---
### Python CLI to quickly Convert & Map Geospatial Data Formats.
#### convert Command
**Input Formats:**   
GeoJSON, GeoPackage, Shapefile, flatgeobuf, H3 JSON  
**Output Formats:**   
GeoJSON, GeoPackage, Shapefile, flatgeobuf   
```bash
# example usage, convert H3 JSON to GeoJSON, use --h3input flag
geopycli convert slope.json geojson --h3input
# convert geojson to GeoPackage  
geopycli convert slope.geojson gpkg
```
#### map command
Send GeoJSON to folium map, opens default browser window.   
Works with polygon, point and line geometry
```bash
# example, send geojson to map 
geopycli map slope.geojson
```
