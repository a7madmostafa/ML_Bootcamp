
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the model
lin_reg = joblib.load("lin_reg.pkl")

# Load the pipeline
full_pipeline = joblib.load("full_pipeline.pkl")

# Load the data
housing = pd.read_csv("https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv")

# Create a title and sub-title
st.title("California Housing Price Prediction App")

st.write("""
This app predicts the **California Housing Price**!
""")

# Take the input from the user
longitude = st.slider('longitude', float(housing['longitude'].min()), float(housing['longitude'].max()))
latitude = st.slider('latitude', float(housing['latitude'].min()), float(housing['latitude'].max()))

housing_median_age = st.slider('housing_median_age', float(housing['housing_median_age'].min()), float(housing['housing_median_age'].max()))
total_rooms = st.slider('total_rooms', float(housing['total_rooms'].min()), float(housing['total_rooms'].max()))
total_bedrooms = st.slider('total_bedrooms', float(housing['total_bedrooms'].min()), float(housing['total_bedrooms'].max()))
population = st.slider('population', float(housing['population'].min()), float(housing['population'].max()))
households = st.slider('households', float(housing['households'].min()), float(housing['households'].max()))
median_income = st.slider('median_income', float(housing['median_income'].min()), float(housing['median_income'].max()))

ocean_proximity = st.selectbox('ocean_proximity', ('<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'))

# Store a dictionary into a variable
user_data = {'longitude': longitude,

'latitude': latitude,   
'housing_median_age': housing_median_age,
'total_rooms': total_rooms,
'total_bedrooms': total_bedrooms,
'population': population,
'households': households,
'median_income': median_income,
'ocean_proximity': ocean_proximity}

# Transform the data into a data frame
features = pd.DataFrame(user_data, index=[0])

# Additional transformations
features['rooms_per_household'] = features['total_rooms']/features['households']
features['bedrooms_per_room'] = features['total_bedrooms']/features['total_rooms']
features['population_per_household'] = features['population']/features['households']

# Pipeline
features_prepared = full_pipeline.transform(features)

# Predict the output
prediction = lin_reg.predict(features_prepared)[0]

# Set a subheader and display the prediction
st.subheader('Prediction')
st.markdown('''# $ {} '''.format(round(prediction), 2))
