import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.header("Aircraft movements in Canada")

@st.cache
def fetch_data():
    data = pd.read_csv(
        "./data/movement_data.csv",
    )
    data = data[data["REF_DATE"]>="2010-01"]

    return data

data = fetch_data()

airports = data["Airports"].unique()
airports.sort()
default_index = np.where(airports == "Total, all airports")[0][0]

option = st.selectbox(
    label="Please select one option below.",
    options=airports,
    index = int(default_index)
)

selection = data[data["Airports"] == option]

fig = px.histogram(selection, 
    x="REF_DATE", 
    y="VALUE", 
    color="Domestic and international itinerant movements",
    nbins=len(selection["REF_DATE"].unique()),
    )

fig.update_layout(legend=dict(
    yanchor="top",
    y=-0.2,
    xanchor="left",
    x=0.2
))

st.plotly_chart(fig, use_container_width=True)
