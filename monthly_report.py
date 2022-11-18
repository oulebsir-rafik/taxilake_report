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


# create a function to compute the big numbers of the report
def big_num(gains_month):
    """ This function takes dataframe of earnings of one month and return the big number of datapane report"""

    # ----------------------------------- creating the big Numbers ---------------------------------------
    # initialize some essential values
    com_name = {"HV0003": "Uber",
                "HV0004": "Via",
                "HV0005": "Lyft"}


    # create a dict to add values of the big numbers
    total_pay_sum = dict()

    # append the values of each company
    for key in com_name.keys():
        total_pay_sum[com_name[key]] = gains_month[gains_month["hvfhs_license_num"] == key]["driver_pay"].sum()


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

    return bigN
#-------------------------------------------------------------------------------------------------




# function that will create a report for a certain company
def company_report(comp_gains, nyc_gjson, company_name):
    """ This function takes a earnings dataframe and dataframe of shape file and 
    return a list of modules to create a report using datapane"""

    # create dataframe of all driver pay
    zone_gains = comp_gains[["pulocationid", "driver_pay"]]
    zone_gains = zone_gains.groupby(["pulocationid"]).sum()
    zone_gains = zone_gains.reset_index()

    # merge the zone_gains dataframe with nyc_gjson dataframe
    zone_gains = pd.merge(zone_gains, nyc_gjson, on=["pulocationid"])

    # create the plots
    daily_avg_plot = daily_avg_bar(comp_gains)
    month_sum_plot = month_sum_donut(comp_gains)
    top_zone = top10_zone(zone_gains)
    map_zone = map_zone_gains(zone_gains)

    return dp.Group(dp.Plot(map_zone),
            dp.Group(dp.Plot(daily_avg_plot),dp.Plot(month_sum_plot),columns = 2),
            dp.Plot(top_zone), label = company_name +  " dataset")


# ---------------------   Creation of the report -----------------------------------

def earning_report(gains_month, nyc_gjson, month_name, year):
    """ this function takes two dataframes and create a complete report using multiple function 
    created in this python script"""

    # initialize the list of dataframes
    list_comp_gains = {}

    for company_code, company_name in zip(["HV0003", "HV0004", "HV0005"], ["Uber", "Via", "Lyft"]):
        # filter dataframe with the company name
        list_comp_gains[company_name] = gains_month[gains_month["hvfhs_license_num"] == company_code]

    # create the big numbers datapane component
    bigN = big_num(gains_month)

    # create the different pages of the finale report
    uber_page = company_report(list_comp_gains["Uber"], nyc_gjson, "Uber")
    lyft_page = company_report(list_comp_gains["Lyft"], nyc_gjson, "Lyft")
    via_page = company_report(list_comp_gains["Via"], nyc_gjson, "Via")

    # the html code for the head title
    head_title = """<center> <img src="https://github.com/oulebsir-rafik/taxilake_report/blob/main/images/headline.PNG?raw=true" alt="alt text" title="xplore logo" style="display:inline"> </center>"""

    # markdown of the data description
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
                dp.Text("<center><h1>🚕 Taxi report - {month} {year} </h1></center>".format(month = month_name, year = str(year))),
                bigN,
                dp.Select(blocks=[uber_page,via_page, lyft_page]),
                dp.Text(data_desc)
        )

    # save the report to an html file
    app.save("./reports/Report_{month}_{year}.html".format(month = month_name, year = str(year)))


