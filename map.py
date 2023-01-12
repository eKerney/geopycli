from os import error
import folium
import webbrowser
import geopandas as gpd
from typer import style

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

