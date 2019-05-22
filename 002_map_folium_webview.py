# import pandas as pd
import folium
import webview

# Create map object
folium_map = folium.Map(location=[27.7, 85.3],
                        zoom_start=13,
                        tiles="CartoDB dark_matter")

# Create circle marker
folium.CircleMarker(location=[27.7, 85.3], fill=True).add_to(folium_map)

# Generate map
folium_map.save('901_map.html')

# Display Map
webview.create_window('Map Time', '901_map.html')
