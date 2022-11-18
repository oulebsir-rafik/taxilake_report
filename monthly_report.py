# in this python file we create a monthly report using datapane

#import the necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import datapane as dp
from numerize import numerize

# add paths for script research
import sys
sys.path.append('./data/')
sys.path.append('./graphics/')

# import different pages and components of the dashboard
from plots import daily_avg_bar, month_sum_donut, top10_zone, map_zone_gains


#------------------------ Importing the data ----------------------------
# import the earnings data
gains = pd.read_csv("gains.csv")
# Set filepath
shp_path = "./data/taxi_zones.shp"

# Read file using gpd.read_file()
nyc_gjson = gpd.read_file(shp_path)
#-------------------------------------------------------------------------

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

#----------------------  Processing earnings csv file-------------------------

# select january data
gains_jan = gains[gains["month"] == 2]
gains_jan.drop(["year", "month"], axis=1, inplace = True)
# initialize some essential values 
com_name = {"HV0003": "Uber",
            "HV0004": "Via",
            "HV0005": "Lyft"}

# select the company 
company = "HV0005" # Uber

# filter dataframe with the company name
comp_gains = gains_jan[gains_jan["hvfhs_license_num"] == company]

# create dataframe of all driver pay
zone_gains = comp_gains[["pulocationid", "driver_pay"]]
zone_gains = zone_gains.groupby(["pulocationid"]).sum()
zone_gains = zone_gains.reset_index()

# merge the zone_gains dataframe with nyc_gjson dataframe
zone_gains = pd.merge(zone_gains, nyc_gjson, on=["pulocationid"])

#-----------------------------------------------------------------------------


# ----------------------------------- creating the big Numbers ---------------------------------------

# create a dict to add values of the big numbers
total_pay_sum = dict()

# append the values of each company
for key in com_name.keys():
  total_pay_sum[com_name[key]] = gains_jan[gains_jan["hvfhs_license_num"] == key]["driver_pay"].sum()


# create the big number in datapane
com_head = [key for key in total_pay_sum.keys()]
bigN = dp.Group(
        dp.BigNumber(
            heading= com_head[0] + " total driver pay",
            value= numerize.numerize(total_pay_sum[com_head[0]]) + " $",
        ),
         dp.BigNumber(
            heading= com_head[1] + " total driver pay",
            value= numerize.numerize(total_pay_sum[com_head[1]]) + " $",
        ),
         dp.BigNumber(
            heading= com_head[2] + " total driver pay",
            value= numerize.numerize(total_pay_sum[com_head[2]]) + " $",
        ),
        columns=3,
    )

#-------------------------------------------------------------------------------------------------

# create the plots
daily_avg_plot = daily_avg_bar(comp_gains)
month_sum_plot = month_sum_donut(comp_gains)
top_zone = top10_zone(zone_gains)
map_zone = map_zone_gains(zone_gains)


head_title = """<center> <img src="./images/headline.png" alt="alt text" title="xplore logo" style="display:inline"> </center>"""


data_desc = """## Data Description 
- **base_passenger_fare**  : base passenger fare before tolls, tips, taxes, and fees.
- **tolls** : the total amount of all tolls paid in trip.
- **bcf** : the total amount collected in trip for Black Car Fund.
- **sales_tax** : the total amount collected in a trip for NYS sales tax.
- **congestion_surcharge** : the total amount collected in a trip for NYS congestion surcharge.
- **airport_fee** : $2.50 for both drop off and pick up at LaGuardia, Newark, and John F. Kennedy airports.
- **tips** : the total amount of tips received from the passenger.
- **driver_pay** : the total driver pay (not including tolls or tips and net of commission, surcharges, or taxes).
"""

# add the different plot to datapane report 
app = dp.App(dp.Text(head_title),
            dp.Text("<center><h1>🚕 January Taxi report </h1></center>"),
            bigN,
             dp.Plot(map_zone),
             dp.Group(
                 dp.Plot(daily_avg_plot),
                 dp.Plot(month_sum_plot),
                 columns = 2),
            dp.Plot(top_zone),
            dp.Text(data_desc)
)

# save the report to an html file
app.upload(name="My example report")
#app.save("Report Jan.html")
