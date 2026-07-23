# Streamlit App for Covid-19 Data Analysis

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
import helper

# Load Data
df = helper.load_data()

# Intro
st.title('Covid-19 Data Analysis')
st.markdown('''
This app is created to analyze the Covid-19 data.
''')

# Country selection
country_options = st.selectbox('Select Country', ['All Countries', 'Select Countries'])
if country_options == 'All Countries':
    countries = 'All Countries'
else:
    countries = st.multiselect('Select', df['Country'].unique())


# Date selection
start_date = st.date_input('Start date', datetime(2020, 1, 1))
start_date = pd.to_datetime(start_date)
end_date = st.date_input('End date', datetime(2023, 1, 1))
end_date = pd.to_datetime(end_date)

# Display Total Cases
st.header('Total Cases')
total_cases = helper.countries_total_cases(countries, start_date, end_date)
st.plotly_chart(total_cases)

# Display Total Deaths
st.header('Total Deaths')
total_deaths = helper.countries_total_deaths(countries, start_date, end_date)
st.plotly_chart(total_deaths)