import pandas as pd

def process_data(df):
    cols = [
        "REF_DATE",
        "Airports",
        "Domestic and international itinerant movements",
        "Type of operation",
        "VALUE"
    ]
    return df[cols]

def compute_total(df):
    airports = df[df["Airports"] != "Total, all airports"]

    total = airports.groupby(["Domestic and international itinerant movements", "Type of operation", "REF_DATE"]).sum().reset_index()

    total["Airports"] = "Total, all airports"

    return pd.concat([airports, total], ignore_index=True)

if __name__ == "__main__":
    old_data = pd.read_csv(
        "../data/23100008.csv",
        dtype={
            "TERMINATED": "str"
        }
    )
    new_data = pd.read_csv(
        "../data/23100302.csv",
        dtype={
            "TERMINATED": "str"
        }
    )


    old_data = process_data(old_data)
    old_data = old_data[old_data["REF_DATE"] < "2019-01"]

    # Handling some special cases
    old_data["Airports"] = old_data["Airports"].str.replace("\n","")
    old_data["Airports"] = old_data["Airports"].str.replace("Whitehorse International, Yukon","Whitehorse/Erik Nielsen International, Yukon")

    old_airports = old_data["Airports"].unique().tolist()

    new_data = process_data(new_data)
    new_data["VALUE"] = new_data["VALUE"].fillna(0).astype(int)
    new_data = new_data[new_data["Airports"].isin(old_airports)]

    old_total = compute_total(old_data)
    new_total = compute_total(new_data)

    movement_data = pd.concat([old_total, new_total], ignore_index=True).sort_values(by=[
             "REF_DATE",
             "Airports",
             "Domestic and international itinerant movements",
             "Type of operation"
    ])

    movement_data.to_csv("../data/movement_data.csv", index=False)