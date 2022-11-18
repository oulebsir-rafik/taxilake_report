import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

with open('Report Jan.html', 'r') as f:
    html_string = f.read()

# embed streamlit docs in a streamlit app
components.html(html_string ,width= 1200, height = 2500, scrolling=True)
