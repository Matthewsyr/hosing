import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Title of the app
st.title('Housing Data Visualization')

# Load the housing dataset
df = pd.read_csv('housing.csv')  # Update with the correct path

# Price slider: Set the range based on the dataset
price_min, price_max = df['median_house_value'].min(), df['median_house_value'].max()
price_filter = st.slider('Select Median House Value Range:', price_min, price_max, (price_min, price_max))

# Multi-select for ocean proximity (location types)
location_types = df['ocean_proximity'].unique()
location_filter = st.sidebar.multiselect(
    'Select Location Type',
    location_types,
    location_types  # Default to all types
)

# Input form for filtering by income level
form = st.sidebar.form("income_form")
income_filter = form.selectbox('Select Income Level', ['All', 'Low (≤2.5)', 'Medium (> 2.5 & < 4.5)', 'High (> 4.5)'])
form.form_submit_button("Apply")

# Filter by median house value
filtered_df = df[(df['median_house_value'] >= price_filter[0]) & (df['median_house_value'] <= price_filter[1])]

# Filter by ocean proximity
filtered_df = filtered_df[filtered_df['ocean_proximity'].isin(location_filter)]

# Filter by income level
if income_filter == 'Low (≤2.5)':
    filtered_df = filtered_df[filtered_df['median_income'] <= 2.5]
elif income_filter == 'Medium (> 2.5 & < 4.5)':
    filtered_df = filtered_df[(filtered_df['median_income'] > 2.5) & (filtered_df['median_income'] < 4.5)]
elif income_filter == 'High (> 4.5)':
    filtered_df = filtered_df[filtered_df['median_income'] > 4.5]

# Show the map
st.header("Housing Map")
st.map(filtered_df[['latitude', 'longitude']])  # Assuming 'latitude' and 'longitude' are in your dataset

# Show dataframe details
st.subheader('Filtered Housing Data:')
st.write(filtered_df[['longitude', 'latitude', 'median_house_value', 'ocean_proximity', 'median_income']])

# Show a histogram of median house values
st.subheader('Histogram of Median House Values')
fig, ax = plt.subplots(figsize=(10, 5))
plt.hist(filtered_df['median_house_value'], bins=30, color='blue', alpha=0.7)
plt.title("Distribution of Median House Values")
plt.xlabel("Median House Value")
plt.ylabel("Frequency")
st.pyplot(fig)