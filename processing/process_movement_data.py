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

if __name__ == "__main__":
    movement_data = pd.read_csv(
        "../data/23100008.csv",
        dtype={
            "TERMINATED": "str"
        }
    )

    movement_data = process_data(movement_data)
    movement_data["Airports"] = movement_data["Airports"].str.replace("\n","")  # to handle the Red Deer Regional case
    movement_data.to_csv("../data/movement_data.csv", index=False)