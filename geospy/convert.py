import geopandas as gpd
import folium

# Load the GeoDataFrame from the .gpkg file
gdf = gpd.read_file('jabo.gpkg')

# Create a basic Folium map centered at [-6.2088, 106.8456]
m = folium.Map(location=[-6.2088, 106.8456], zoom_start=10)

# Define a style function
def style_function(feature):
    return {
        'fillColor': 'red',
        'color': 'black',
        'weight': 0,
        'opacity': 1,
        'fillOpacity': 0.6
    }

# Add GeoJson data to the map with the style function
folium.GeoJson(
    gdf,
    style_function=style_function,
).add_to(m)

# Save the map as an HTML file
m.save('mapyes.html')
