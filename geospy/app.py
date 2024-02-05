from flask import Flask, render_template, request
import geopandas as gpd
import folium
from branca.colormap import linear

app = Flask(__name__)

# Load the given gpkg file.
gdf = gpd.read_file('jabo.gpkg')

# Convert relevant fields to numeric. Basically only fields that are numbers and bukan string. 
numeric_fields = [
    'pop', 'payload_mbyte_gh7', 'revenue_gh7',
    'subscriber_gh7', 'payload_growth_pct', 'market_share_pct', 'pop_index',
    'growth_index', 'payload_index', 'revenue_index', 'market_share_index',
    'hot_spot_index', 'normalized_score', 'normalized_normalized_score'
]
gdf[numeric_fields] = gdf[numeric_fields].apply(lambda x: gpd.pd.to_numeric(x))

# This is for the default route pas we open localhost. It displays the index.html for this page. 
@app.route('/')
def index():
    return render_template('index.html', criteria=numeric_fields, selected_criteria=None, selected_filter_values=None)

# This is after we click filter (or search).
@app.route('/filter', methods=['POST'])
def filter():
    criteria = []
    filter_values = []

    # Iterates through the filters atau search criteria. 
    for i in range(1, 4):
        criterion = request.form.get(f'criteria{i}')
        value = request.form.get(f'filter_value{i}')

        if criterion != 'none' and value:
            criteria.append(criterion)
            filter_values.append(float(value))

    # Apply filter criteria to the data frame. 
    filtered_gdf_filter = gdf.copy()

    # Filters.
    for criterion, filter_value in zip(criteria, filter_values):
        filtered_gdf_filter = filtered_gdf_filter[filtered_gdf_filter[criterion] >= filter_value]

    # Search criteria for "Kabupaten" and "kab_cluster"
    kabupaten_search = request.form.get("kabupaten_search")
    kab_cluster_search = request.form.get("kab_cluster_search")

    # These next two code clusters are basically only for searching. Masih harus abstract if we want to search for more things.
    # Filter by "Kabupaten" search
    if kabupaten_search:
        filtered_gdf_kabupaten = gdf[gdf['kabupaten'].str.contains(kabupaten_search, case=False, na=False)]
    else:
        filtered_gdf_kabupaten = gdf  # No search, include all

    # Filter by "kab_cluster" search
    if kab_cluster_search:
        filtered_gdf_kab_cluster = gdf[gdf['kab_cluster'].str.contains(kab_cluster_search, case=False, na=False)]
    else:
        filtered_gdf_kab_cluster = gdf  # No search, include all

    # Combine the results of filter and search
    filtered_gdf = filtered_gdf_filter[filtered_gdf_filter.index.isin(filtered_gdf_kabupaten.index) & filtered_gdf_filter.index.isin(filtered_gdf_kab_cluster.index)]

    # Create a basic Folium map
    m = folium.Map(location=[-6.2088, 106.8456], zoom_start=10)

    # Create colormap and style based on the filtered data
    colormap = linear.Reds_09.scale(0, 1).to_step(100)

    # Function for map styling. 
    def style_function(feature):
        properties = feature['properties']
        pass_filter = True  # Variable to check if the feature passes the filter

        for criterion, filter_value in zip(criteria, filter_values):
            value = properties[criterion]

            if isinstance(value, (int, float)):
                if value < filter_value:
                    pass_filter = False
                    break  # Exit the loop early if the feature fails any filter criterion
            else:
                pass_filter = False
                break  # Non-numeric values automatically fail the filter

        if pass_filter:
            # If the feature passes all criteria, return the style
            color = colormap(max(value for value in properties.values() if isinstance(value, (int, float))))
            return {
                'fillColor': 'red',
                'color': 'black',
                'weight': 0,
                'opacity': 1,
                'fillOpacity': 0.6
            }
        else:
            # If the feature doesn't pass the filter, return a transparent style
            return {
                'fillColor': 'transparent',
                'color': 'transparent',
                'weight': 0,
                'opacity': 0,
                'fillOpacity': 0
            }




    # Add filtered data to the map
    folium.GeoJson(
        filtered_gdf,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=['region', 'kabupaten', 'kab_cluster', 'pop', 'payload_mbyte_gh7', 'revenue_gh7',
                            'subscriber_gh7', 'payload_growth_pct', 'market_share_pct', 'pop_index',
                            'growth_index', 'payload_index', 'revenue_index', 'market_share_index',
                            'hot_spot_index', 'normalized_score', 'normalized_normalized_score'],  labels=True, sticky=False)
    ).add_to(m)

    # Convert the map to HTML and pass it to the template
    map_html = m._repr_html_()

    return render_template('index.html', criteria=numeric_fields, selected_criteria=criteria, selected_filter_values=filter_values, map=map_html)

if __name__ == '__main__':
    app.run(debug=True)
