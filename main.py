import pandas as pd
import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as components

# add paths for script research
import sys
sys.path.append('.')

from monthly_report import earning_report

#------------------------ Importing the data ----------------------------
# import the earnings data
gains = pd.read_csv("./data/gains.csv")
# Set filepath
shp_path = "./data/taxi_zones.shp"

# Read file using gpd.read_file()
nyc_gjson = gpd.read_file(shp_path)

#----------------------- Processing shape file data ----------------------
# drop some columns
nyc_gjson.drop(["OBJECTID", "Shape_Leng", "Shape_Area"], axis=1, inplace = True)
# create the full name of the zone
nyc_gjson["zone_full_name"] = nyc_gjson["borough"] + " - " + nyc_gjson["zone"]
# copy  locationId column to pulocationid columns to change the name
nyc_gjson["pulocationid"] = nyc_gjson["LocationID"]
# drop the uncessary columns
nyc_gjson.drop(["LocationID", "zone", "borough"], axis=1, inplace=True)
#---------------------------------------------------------------------------


#set the layout to wide
st.set_page_config(layout="wide")

st.markdown("<center> <h1>📄 Report Generator </h1> </center>", unsafe_allow_html=True)


st.markdown("<h4> This streamlit application allow you to create report on taxi data of new york </h4>",
            unsafe_allow_html=True)

# data initialization
months = {"January" : 1, "February" : 2, "March" : 3, "April" : 4,
          "May" : 5, "June" : 6, "July" : 7, "August" : 8, "September" : 9,
          "October" : 10, "November" : 11, "December": 12}

year = [2021]


col1, col2 = st.columns(2)

year_sel = col1.selectbox("Select the year", year)
month_sel = col2.selectbox("Select the month", list(months.keys()))

generate = st.button('Generate Report')

if generate:
    #----------------------  Processing earnings csv file-------------------------
    # filter data
    gains_month = gains[gains["month"] == months[month_sel]]
    gains_month.drop(["year", "month"], axis=1, inplace = True)

    earning_report(gains_month, nyc_gjson, month_sel, year_sel)
    
    html_file = open('./reports/Report_{month}_{year}.html'.format(month = month_sel, year = str(year_sel)), 'rb')
    html_string = html_file.read()
    
    st.markdown("<center><h2>Preview of the report</h2></center>", unsafe_allow_html=True)

    btn = st.download_button(
            label="Download the html file",
            data=html_file,
            file_name="taxi_report.html"
          )
    #embed streamlit docs in a streamlit app
    components.html(html_string ,width= 1200, height = 800, scrolling=True)
