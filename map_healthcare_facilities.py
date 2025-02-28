import pandas as pd
import geopandas as gpd
import os
import folium
from folium.plugins import MarkerCluster

# create basemap for hospital plot
base_map = folium.Map(location=[35.5, -78.8], zoom_start=8, tiles='OpenStreetMap')


# financial information on individual hospitals
# https://tool.nashp.org/
financial_data = pd.read_excel('NASHP 2011-2023 HCT Data 2024 Dec.xlsx', sheet_name = 'Downloadable')
# slice dataframe to include only NC hospitals
nc_financial = financial_data[financial_data['State'] == 'NC']
hospital_list = nc_financial['Hospital Name'].unique() # list of hospital names

# location of medical facilities in NC
# https://www.nconemap.gov/datasets/nconemap::medical-facilities/explore
medf_path = 'Medical_Facilities/Medical_Facilities.shp'
medfacilities = gpd.read_file(medf_path)
# convert geospatial data to lat/long coordinates
medfacilities = medfacilities.to_crs(epsg=4326)
facility_types = medfacilities['stype'].unique()# list of medical facility types

# initialize a dictionary to store each layer of the map
# each facility type will display as its own layer
facility_type_layers = {}
for facility in facility_types:
  # set default layer (which one is visible when you load the map)
  if facility == 'Hospital':
    show_layer = True
  else:
    show_layer = False
  # each folium FeatureGroup will correspond to one layer
  # these are stored in this dictionary and added to the base_map at the end
  facility_type_layers[facility] = folium.FeatureGroup(name=facility, show = show_layer)

# loop through each medical facility in the database
# for each facility, create:
# a map marker (icon)
# a popup plot that comes up when you click on the marker
# and the lat/long coefficients for the facility 
for index, row in medfacilities.iterrows():
  # for hospitals, use financial data and a 'hospital' marker
  if row['stype'] medfacilities 'Hospital':
    icon = folium.Icon(color="red", icon="hospital", prefix = 'fa')#hospital marker
    # popup plots are previously generated .html files
    # these plots are created with the script make_healthcare_popups.py
    popup_path = os.path.join('FinancialFigures', row['facility'], 'operating_income_small.html')
    # not all facilities have medical data use try/except to look for the right file
    no_financial_data = False
    try:
      # if there is a file at the path, open and use as the popup
      with open(popup_path, encoding="utf8") as f:
        html = f.read()
      # popup is just an IFrame wrapper around an html file
      popup = folium.Popup(folium.IFrame(html, width=600, height=300), max_width=1000)
    except: 
      no_financial_data = True
    # set popup/icon for hospitals w/o financial data
    # icon is set to gray so we can tell how many facilities we have data for
    if no_financial_data:
      popup = folium.Popup(row['facility'], max_width=1000)
      icon = folium.Icon(color="gray", icon="hospital", prefix = 'fa')
  else:
    # all other facilities get default markers with no popup
    icon = folium.Icon(color="blue", icon="user-doctor", prefix = 'fa')
    popup = folium.Popup(row['facility'], max_width=1000)
  
  # create markers for each facility, adding icon and popup created above  
  facility_marker = folium.Marker(location = [row['geometry'].y, row['geometry'].x], popup = popup, icon = icon)
  # add the facilities to the corresponding layers
  facility_marker.add_to(facility_type_layers[row['stype']])

# add each layer (facility types) to the base_map
for facility in facility_types:
  base_map.add_child(facility_type_layers[facility])
# add a toggle button for the layers
base_map.add_child(folium.LayerControl())
# save map as html file
base_map.save("healthcare_facilities.html")
