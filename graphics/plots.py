# import the necessary libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

#create an plolty graph to display the average of earnings parameters
def daily_avg_bar(comp_gains):
    """ This function get the earnings data of one company in new york and return plolty bar plot"""
    # sum of some parameter
    daily_avg_df = comp_gains.mean().drop(["pulocationid"])

    # transform the series to dataframe using to_frame()
    daily_avg_df = daily_avg_df.to_frame().reset_index()

    # Rename the columns
    daily_avg_df.columns = ["parameter", "daily_average"]
    
    # create a dictionnary that store the parameters of the plolty bar plot
    daily_avg_template = {
    "layout": go.Layout(
        # general font parameters
        font={
            "family": "Verdana",
            "size": 12,
            "color": "#707070",
        },
        # title parameters
        title={
            "font": {
                "family": "Tahoma",
                "size": 20,
                "color": "#1f1f1f",
            }
        },
        # background plot color
        plot_bgcolor="#e6f9ff"
        )
    }

    # plot the bar plot using plolty express
    daily_avg_plt = px.bar(daily_avg_df, x='parameter', y='daily_average', 
                           text_auto='.2s',
                           title = "<b> Daily average of earnings </b>",
                           template=daily_avg_template) # add the parameter to the template

    # change some plot parameters
    daily_avg_plt.update_xaxes(tickangle=40, title=None)
    daily_avg_plt.update_yaxes(title="Earnings ($)")
    daily_avg_plt.update_traces(textfont_size=12, textangle=0)

    return daily_avg_plt


# function that create a donut chart of different earnings
def month_sum_donut(comp_gains):
    """ This function get the earnings data of one company in new york and return monthly sum donut plot """

    # create dataframe to make the donut
    donut_df = comp_gains.sum().drop(["date", "pulocationid", "hvfhs_license_num", "driver_pay"])
    # calculate the total revenue for each columns
    total_revenue = donut_df.sum()
    donut_df = donut_df * (100/total_revenue)
    # round the values
    donut_df = donut_df.apply(lambda x: round(x,2))
    # transform the series to dataframe
    donut_df = donut_df.to_frame().reset_index()
    # rename the columns
    donut_df.columns = ["parameter", "percentage of monthly total revenue"]

    donut_template = {
    "layout": go.Layout(
        title={
            "font": {
                "family": "Tahoma",
                "size": 20,
                "color": "#1f1f1f"
            },
            'y':0.9, # new
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'  
            }
        )
    }

    # create the donut plot using plotly
    donut_plot = px.pie(donut_df, 
             values='percentage of monthly total revenue', 
             names='parameter',
             title= "<b> Pie chart of all revenues </b>",      
             color_discrete_sequence=px.colors.sequential.Aggrnyl,
             template=donut_template)

    return donut_plot


# function that create a bar plot of top 10 zones with highest revenue
def top10_zone(zone_comp_gains):
    """ This function takes dataframe of earnings of a company with geometries and locations and return a barplot"""
    # get the data that we needs
    zone_bar_df = zone_comp_gains[["pulocationid", "driver_pay", "zone_full_name"]].copy()
    # sort the values
    zone_bar_df.sort_values("driver_pay", ascending=False, inplace=True)

    # get the top 10 locations
    zone_bar_df = zone_bar_df.iloc[:10,:]

    # create a dictionnary that store the parameters of the plolty bar plot
    top10_template = {
    "layout": go.Layout(
        # general font parameters
            font={
                "family": "Verdana",
                "size": 12,
                "color": "#707070",
            },
            # title parameters
            title={
                "font": {
                "family": "Tahoma",
                "size": 20,
                "color": "#1f1f1f",
                }
            },
            # background plot color
            plot_bgcolor="#e6f9ff"
        )
    }

    # create the plolty bar plot 
    zone_bar_plot = px.bar(zone_bar_df, x='zone_full_name', y='driver_pay', 
                       text_auto='.2s', 
                       title = "<b>Top 10 zones with highest earnings </b>",
                       width=900, height=400,
                       template=top10_template) # include the layout template

    # change some parameters of the layout
    zone_bar_plot.update_xaxes(tickangle=40, title=None)
    zone_bar_plot.update_yaxes(title="Driver Pay ($)")
    zone_bar_plot.update_traces(textfont_size=12, textangle=0)
    zone_bar_plot.update_layout(margin={"r": 60, "t": 50, "l": 100, "b": 140})

    return zone_bar_plot


# function that will map the earnings of each zone
def map_zone_gains(zone_comp_gains):
    """ this function takes dataframe of earnings of a company with geometries
    and transform it into geopandas dataframe and return a choropleth map"""
    # convert the dataframe to geodataframe
    zone_gains_gdf = gpd.GeoDataFrame(zone_comp_gains, geometry="geometry")

    # change the projection system
    zone_gains_gdf = zone_gains_gdf.to_crs("WGS84")

    # creating a map using plotly
    zone_map = px.choropleth_mapbox(zone_gains_gdf,
                                    geojson=zone_gains_gdf["geometry"],
                                    locations=zone_gains_gdf.index,
                                    color="driver_pay",
                                    center={"lat": 40.730610, "lon": -73.935242},
                                    mapbox_style="carto-positron",
                                    color_continuous_scale = px.colors.sequential.Sunsetdark,
                                    opacity=0.7,
                                    hover_data=["zone_full_name", "driver_pay"],
                                    title = "<b> Map of earnings by zone </b>",  
                                    width=400, height=600,
                                    zoom=9)

    # updating the layout to make the map more readable 
    zone_map.update_layout(margin={"r": 220, "t": 80, "l": 220, "b": 0})
    # updating the layout to add title
    zone_map.update_layout(
        title={
                "font": {
                    "family": "Tahoma",
                    "size": 20,
                    "color": "#1f1f1f"
                },
                'y':0.93, # new
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            })

    # updating the layout to style the legend title
    zone_map.update_layout(
        coloraxis_colorbar = {
                "title" : "<b>Driver pay ($)</b>"
            })

    return zone_map