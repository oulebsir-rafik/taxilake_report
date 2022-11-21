# 🧾 NYC Report Generator

In this repo, i created a streamlit app that generate report of the revenues of the different taxi companies in New York. You can find the original dataset here ([New york taxi data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)).

![demo of the report](./md_image/report_demo.gif)

## Datasets
The dataset used in this streamlit app is an aggregated data of **The high volume For-Hire Vehicle** measured in 2021. You can find the data used in this app in the *data* folder, but we invite the user to try to connect this streamlit app to a storage service **(like AWS S3 our Google cloud storage)**.

## How to use

In order to use this app, you need to clone the repo:
``git clone https://github.com/oulebsir-rafik/taxilake_report``

install th necessary libraries :
``pip install -r requirements.txt``

run the streamlit app:
``streamlit run main.py ``