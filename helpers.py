import streamlit as st
import pandas as pd
from typing import Dict
from dataclasses import dataclass
import plotly.express as px
import plotly.graph_objects as go

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

@st.cache
def fetch_data(table):
    df = pd.read_csv(f"./data/{table}.csv")
    return df

def display_hist(df, airport, code):

    df1 = df.groupby(by = ["REF_DATE", "Domestic and international itinerant movements"], as_index=False).sum()
    df2 = df.groupby(by = ["REF_DATE", "Type of operation"], as_index=False).sum()

    trace1 = px.bar(
        df1,
        x="REF_DATE",
        y="VALUE",
        color="Domestic and international itinerant movements",
        title="Trace 1"
    )

    trace2 = px.bar(
        df2,
        x="REF_DATE",
        y="VALUE",
        color="Type of operation",
        title="Trace 2"
    )

    fig = go.Figure()

    fig.add_traces(trace1.data)
    fig.add_traces(trace2.data)

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                showactive=True,
                x=1.0,
                y=1.16,
                buttons=list(
                    [
                        dict(
                            label="By сonnection type",
                            method="update",
                            args=[
                                {"visible": [True, True, True, False, False, False, False, False, False]}
                            ]
                        ),
                        dict(
                            label="By operation type",
                            method="update",
                            args=[
                                {"visible": [False, False, False, True, True, True, True, True, True]}
                            ]
                        )
                    ]
                )
            )
        ]
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
        )
    )

    for trace in fig.data:
        if trace["hovertemplate"].startswith("Type of operation"):
            trace.update(visible=False)

    fig.update_layout(
        barmode="stack",
        xaxis_title="Date",
        yaxis_title="Count",
    )

    if airport == "Total, all airports":
        fig_title = airport
    else:
        fig_title = f"{airport} (ICAO: {code})"

    fig.update_layout(
        title=dict(
            text=fig_title,
            x=0.5,
            font={"size": 20}
        )
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.0,
    ))

    st.plotly_chart(fig, use_container_width=True)

def display_ranking(df):
    fig = go.Figure()

    trace = px.bar(
        df,
        x="VALUE",
        y="Airports",
        orientation="h"
    )
    fig.add_traces(trace.data)

    fig.update_layout(xaxis_title="Count")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig, use_container_width=True)