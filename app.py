from re import U
import streamlit as st
from streamlit_folium import st_folium
import folium
from typing import Optional
from helpers import Point, fetch_data, display_hist, display_ranking
from pathlib import Path

st.set_page_config(layout="wide")

_, headcol, _ = st.columns([1,4,1])
with headcol:
    st.image("./data/header.png", use_column_width=True)

movement_data = fetch_data(table = "movement_data")
airport_data = fetch_data(table = "airport_icao_codes")

page = st.sidebar.radio(
    label = "sidebarRadio",
    options=[
        "Historical data",
        "Ranking",
        "Glossary"
    ],
    label_visibility="collapsed"
)

if page == "Historical data":

    _, _, _, radio_column = st.columns(4)
    with radio_column:
        radio = st.radio(
            label="radio",
            options=[
                "List",
                "Map"
            ],
            horizontal=True,
            label_visibility="collapsed"
        )

    if radio == "List":
        airport_selected = st.selectbox(
            "Select airport from the list below",
            (movement_data["Airports"].unique()),
        )

        selection = movement_data[movement_data["Airports"] == airport_selected]
        selection = selection[selection["Type of operation"] != "Total itinerant movements"]

        icao_code_selected = None
        if airport_selected != "Total, all airports":
            icao_code_selected = airport_data[airport_data["Airport"] == airport_selected]["ICAO_OACI"].values[0]

        display_hist(selection, airport_selected, code=icao_code_selected)

    if radio == "Map":
        m = folium.Map(location=[56, -94], zoom_start=4)
        for i in range(len(airport_data)):
            lat = airport_data["LATTITUDE"][i]
            lon = airport_data["LONGITUDE"][i]
            tooltip = f"{airport_data['Airport'][i]} <br>ICAO: {airport_data['ICAO_OACI'][i]}"
            folium.Marker([lat, lon], tooltip=tooltip).add_to(m)

        map_data = st_folium(m, width=1000, height=400)

        try:
            point_clicked: Optional[Point] = Point.from_dict(map_data["last_object_clicked"])
            lat = point_clicked.lat
            lon = point_clicked.lon
            clicked = airport_data[(airport_data["LATTITUDE"] == lat) &
                                    ((airport_data["LONGITUDE"] == lon))].to_dict("records")[0]

            airport_clicked = clicked["Airport"]
            icao_code_clicked = clicked["ICAO_OACI"]

            selection = movement_data[movement_data["Airports"] == airport_clicked]
            selection = selection[selection["Type of operation"] != "Total itinerant movements"]

            display_hist(df=selection, airport=airport_clicked, code=icao_code_clicked)

        except TypeError:
            point_clicked = None

if page == "Ranking":

    MonthDict={
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }

    min_date = movement_data["REF_DATE"].min()
    max_date = movement_data["REF_DATE"].max()

    min_year, min_month = min_date.split("-")
    max_year, max_month = max_date.split("-")
    min_year = int(min_year)
    max_year = int(max_year)
    min_month = int(min_month)
    max_month = int(max_month)

    yearList = [*range(min_year, max_year+1)]

    group = st.selectbox(
        "Please select one category in the selection box below and relevant period",
        (
        "Total movements",
        "Domestic movements",
        "Other international movements",
        "Transborder movements",
        "Air carrier movements, level I-III including foreign air carriers",
        "Air carrier movements, level IV-VI",
        "Other commercial movements",
        "Private movements",
        "Government civil movements",
        "Government military movements"
        )
    )

    col1, col2, pad2, col3, col4 = st.columns((10,10,10,10,10))

    with col1:
        year_from = st.selectbox("From", yearList, yearList.index(min_year), key="YF")
    with col2:
        month_from = st.selectbox("", MonthDict, index=list(MonthDict.values()).index(min_month) ,key="YT")
    with col3:
        year_to = st.selectbox("To", yearList, index=yearList.index(max_year), key="MF")
    with col4:
        month_to = st.selectbox("", MonthDict, index=list(MonthDict.values()).index(max_month), key="MT")

    start = f"{year_from}-{MonthDict[month_from]:02d}"
    end = f"{year_to}-{MonthDict[month_to]:02d}"

    selection = movement_data[movement_data["Airports"] != "Total, all airports"]
    selection = selection[selection["Type of operation"] != "Total itinerant movements"]

    if group in ["Domestic movements","Other international movements","Transborder movements"]:
        selection = selection[selection["Domestic and international itinerant movements"] == group]

    if group in ["Air carrier movements, level I-III including foreign air carriers",
        "Air carrier movements, level IV-VI",
        "Other commercial movements",
        "Private movements",
        "Government civil movements",
        "Government military movements"]:
        selection = selection[selection["Type of operation"] == group]

    selection = selection[(selection['REF_DATE'] >= start) & (selection['REF_DATE'] <= end)]
    selection = selection.groupby(by=["Airports"], as_index=False).sum()
    selection = selection.sort_values(by="VALUE", ascending=False).head(10)

    display_ranking(selection)

if page == "Glossary":
    glossary = Path("./data/glossary.md").read_text()
    st.markdown(glossary)