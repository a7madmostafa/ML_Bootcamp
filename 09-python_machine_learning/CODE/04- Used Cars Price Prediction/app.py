
import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title('Used Cars Price Prediction')

# Load Data for Deployment
data = pickle.load(open('data_for_deploy.pkl', 'rb'))

# Input Data
car_brand = st.selectbox('Brand', data['brands'].keys())
car_model = st.selectbox('Model', data['brands'][car_brand])
fuel_type = st.selectbox('Fuel Type', data['fuel_types'][car_model])
transmission = st.selectbox('Transmission', data['transmissions'][car_model])
seats = st.selectbox('Seats', data['seats'][car_model])

location = st.selectbox('Location', data['locations'])
year = st.selectbox('Year', range(min(data['years']), max(data['years'])+1))
km_driven = st.slider('Kilometers Driven', min_value= 10, max_value=500000, step=1)

owner_type = st.selectbox('Owner Type', data['Owner_Type'])
mileage = st.slider('Mileage', min_value=data['Min_Mileage'], max_value=data['Max_Mileage'])
engine = st.slider('Engine', min_value=data['Min_Engine'], max_value=data['Max_Engine'])
power = st.slider('Power', min_value=data['Min_Power'], max_value=data['Max_Power'])



new_data = pd.DataFrame({'Location': location,
                         'Year': year,
                         'Kilometers_Driven': km_driven,
                         'Fuel_Type': fuel_type,
                         'Transmission': transmission,
                         'Owner_Type': owner_type,
                         'Mileage': mileage,
                         'Engine': engine,
                         'Power': power,
                         'Seats': seats,
                         'Brand': car_brand,
                         'Model': car_model}, index=[0])

# Preprocessing
preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))
new_data_preprocessed = preprocessor.transform(new_data)


# Prediction
model = pickle.load(open('model.pkl', 'rb'))
log_price = model.predict(new_data_preprocessed) # in log scale
price = np.expm1(log_price) # in original scale

# From Lakhs to USD
price_usd = price[0] * data['lakh_to_usd']

# Output
if st.button('Predict'):
    st.header('Predicted Price')
    st.markdown('**Price in USD**: $' + str(round(price_usd, 2)))

