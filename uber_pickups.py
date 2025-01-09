import streamlit as st
import pandas as pd
import numpy as np

# add a title
st.title("Uber pickups in NYC")

# run the app by typing "streamlit run uber_pickups.py" in the terminal

# fetch some data
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# cache the data: you don't have to fetch data every time you update the app
# the annotation tells the streamlit that:
# Whenever the function is called, check 2 things: input parameters and the function code
# if neither of them has changed, skip the function and return the cached result (if there is one)

@st.cache_data
def load_data(nrows):
    """
    fetch uber data from the web
    nrows: how many rows to fetch
    """
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    # convert data type to datetime format
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded. Once the data is loaded, the following text will be displayed
data_load_state.text('Done! (using st.cache_data)')

# st.write tries to render almost everything. 
# When it fails, you can use a more specific function like st.dataframe
# Toggle to display the original data
if st.checkbox('Show raw data'):
    st.subheader("Raw data")
    st.write(data)

# Draw a histogram
st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# plot data on a map (select only one hour)
# filter the result with a slider: min, max, default
hour_to_filter = st.slider('hour', 0, 23, 17) 
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)



