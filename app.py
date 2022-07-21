from typing import Dict, Optional
from dataclasses import dataclass

import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")
@dataclass
class Point:
    lat: float
    lon: float

    @classmethod
    def from_dict(cls, data: Dict) -> "Point":
        if "lat" in data:
            return cls(float(data["lat"]), float(data["lng"]))
        elif "latitude" in data:
            return cls(float(data["latitude"]), float(data["longitude"]))
        else:
            raise NotImplementedError(data.keys())

st.header("Aircraft movements in Canada")

@st.cache
def fetch_data(table):
    df = pd.read_csv(f"./data/{table}.csv")
    return df

movement_data = fetch_data(table = "movement_data")
airport_data = fetch_data(table = "airport_icao_codes")

page = st.sidebar.radio(
    label = "",
    options=[
        "Historical data",
        "Ranking",
        "Glossary"
    ]
)

if page == "Historical data":
    m = folium.Map(location=[56, -94], zoom_start=4)
    for i in range(len(airport_data)):
        lat = airport_data["LATTITUDE"][i]
        lon = airport_data["LONGITUDE"][i]
        tooltip = f"{airport_data['Airport'][i]} <br>ICAO: {airport_data['ICAO_OACI'][i]}"
        folium.Marker([lat, lon], tooltip=tooltip).add_to(m)

    map_data = st_folium(m, width=1000, height=500)

    try:
        point_clicked: Optional[Point] = Point.from_dict(map_data["last_object_clicked"])
        lat = point_clicked.lat
        lon = point_clicked.lon
        airport_clicked = airport_data[(airport_data["LATTITUDE"] == lat) &
                                        ((airport_data["LONGITUDE"] == lon))]["Airport"].values[0]

        selection = movement_data[movement_data["Airports"] == airport_clicked]

        df = selection[selection["Type of operation"] == "Total itinerant movements"].copy()
        df.drop(["Airports", "Type of operation"], axis=1, inplace=True)

        fig = px.bar(
            df,
            x="REF_DATE",
            y="VALUE",
            color="Domestic and international itinerant movements",
            title="Trace 1",
            width=1000,
            height=500
        )

        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1 year",
                            step="year",
                            stepmode="backward"),
                        dict(count=5,
                            label="5 years",
                            step="year",
                            stepmode="backward"),
                        dict(count=10,
                            label="10 years",
                            step="year",
                            stepmode="backward"),
                        dict(
                            label="all available",
                            step="all")
                        ])
                ),
                type="date"
            ),
            legend=dict(
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0.2
            )
        )

        st.plotly_chart(fig)

    except TypeError:
        point_clicked = None