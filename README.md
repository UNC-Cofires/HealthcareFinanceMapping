# HealthcareFinanceMapping
repository for mapping healthcare facilities and viewing financial timeseries data
## Getting Started
This repository requires data from the website https://tool.nashp.org/. Download
the file 'NASHP 2011-2023 HCT Data 2024 Dec.xlsx' from the data download link labeled 'Hospital Level dataset (2011-2023)'
put this file in the HealthcareFinanceMapping repository before running any code

### Dependencies

Python Libraries:

* geopandas
* folium
* difflib
* pandas
* os
* plotly
* numpy
* datetime

### Executing program

* This repository will map healthcare facilities in North Carolina
* each hospital has 'popup' data that shows hospital financial records
* First you must create the plots that go into the popup boxes
* To create these plots run the script:
```
python -W ignore make_healthcare_popup.py
```
* once the popup plots have been created, make maps by running the script:
```
python -W ignore map_healthcare_facilities.py
```



