import pandas as pd
import geopandas as gpd
import difflib
import plotter
# location of medical facilities in NC
# https://www.nconemap.gov/datasets/nconemap::medical-facilities/explore
medf_path = 'Medical_Facilities/Medical_Facilities.shp'
medf = gpd.read_file(medf_path)
medf = medf.to_crs(epsg=4326)

# financial information on individual hospitals
# https://tool.nashp.org/
financial_data = pd.read_excel('NASHP 2011-2023 HCT Data 2024 Dec.xlsx', sheet_name = 'Downloadable')
# slice hospital dataframe to only include the state of north carolina
nc_financial = financial_data[financial_data['State'] == 'NC']
# create list of all unique hospital names
hospital_list = nc_financial['Hospital Name'].unique()

# need to create a dictionary that links hospital names
# from the medical facilities geospatial data with the
# hospital names from the financial reporting 
key_bridge = {}# link from geospatial to financial data
for index, row in medf.iterrows():
  # only look for medical facilities that are hospitals
  if row['stype'] == 'Hospital':
    # loop through all hospitals to look for exact match
    found_match = False
    for hos in hospital_list:
      # record exact matches
      if hos.casefold() == row['facility'].casefold():
        key_bridge[hos] = row['facility']
        found_match = True
        break
    # if no exact match is found, record close matches
    if not found_match:
      # from geospatial data hospital names, find closest hospital names in financial dataset
      word_list = difflib.get_close_matches(row['facility'].upper(), hospital_list, cutoff = 0.85)
      # record closest match
      if len(word_list)> 0:
        key_bridge[word_list[0]] = row['facility']

# patient types are: charity, uninsured, medicaid, CHIP, medicare, medicare advantage, & private
# in financial data, column labels for % of revenue from each type of patient
payment_types = ['Charity Care Payer Mix', 'Uninsured and Bad Debt Payer Mix',
                 'Medicaid Payer Mix', "SCHIP and Low Income Gov't Program Payer Mix",
                 'Medicare Payer Mix', 'Medicare Adv Payer Mix', 'Commercial Payer Mix']
# in financial data, column labels for $ values from each insurance type
operating_ratios = ['Net Charity Care Cost', 'Uninsured and Bad Debt Cost', 
                    'Medicaid Hospital Operating Profit (Loss)',
                    "SCHIP and Low Income Gov't Program Hospital Operating Profit (Loss)", 
                    'Medicare Hospital Operating Profit (Loss)',
                    'Medicare Advantage Hospital Operating Profit (Loss)', 
                    'Commercial Hospital Operating Profit (Loss)']
# make plots                   
plot_colors = ['sienna', 'maroon', 'palevioletred', 'beige', 'goldenrod', 'olive', 'cornflowerblue']
for hospital_name in key_bridge:
  # get financial data for specific hospital
  this_hospital_financial = nc_financial[nc_financial['Hospital Name'] == hospital_name]
  # make financial data plots (these plots are defined in plotter.py file)
  plotter.plot_patient_mix(this_hospital_financial, payment_types, plot_colors, hospital_name, key_bridge[hospital_name])
  plotter.plot_patient_mix_small(this_hospital_financial, payment_types, plot_colors, hospital_name, key_bridge[hospital_name])
  plotter.plot_op_income(this_hospital_financial, operating_ratios, plot_colors, hospital_name, key_bridge[hospital_name])
  plotter.plot_op_income_small(this_hospital_financial, operating_ratios, plot_colors, hospital_name, key_bridge[hospital_name])
