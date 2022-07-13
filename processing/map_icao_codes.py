import pandas as pd

if __name__ == "__main__":

    airport_info = pd.read_csv(
        "../data/Airports_Aeroports.csv",
        encoding = 'unicode_escape'
    )

    # The following dictionary is manually generated using the aircraft movements data
    # and the following resource:
    # https://open.canada.ca/data/en/dataset/3a1eb6ef-6054-4f9d-b1f6-c30322cd7abf

    icao_codes = {
    "Abbotsford, British Columbia":"CYXX",
    "Boundary Bay, British Columbia":"CZBB",
    "Calgary International, Alberta":"CYYC",
    "Calgary/Springbank, Alberta":"CYBW",
    "Chicoutimi/St-Honoré, Quebec":"CYRC",
    "Edmonton City Centre, Alberta":"CYXD",
    "Edmonton International, Alberta":"CYEG",
    "Edmonton/Villeneuve, Alberta":"CZVL",
    "Fort McMurray, Alberta":"CYMM",
    "Fredericton International, New Brunswick":"CYFC",
    "Gander International, Newfoundland and Labrador":"CYQX",
    "Halifax/Robert L. Stanfield International, Nova Scotia":"CYHZ",
    "Hamilton, Ontario":"CYHM",
    "Kelowna, British Columbia":"CYLW",
    "Kitchener/Waterloo, Ontario":"CYKF",
    "Langley, British Columbia":"CYNJ",
    "London, Ontario":"CYXU",
    "Moncton/Greater Moncton International, New Brunswick":"CYQM",
    "Montréal/Mirabel International, Quebec":"CYMX",
    "Montréal/Pierre Elliott Trudeau International, Quebec":"CYUL",
    "Montréal/St-Hubert, Quebec":"CYHU",
    "North Bay, Ontario":"CYYB",
    "Oshawa, Ontario":"CYOO",
    "Ottawa/Macdonald-Cartier International, Ontario":"CYOW",
    "Pitt Meadows, British Columbia":"CYPK",
    "Prince George, British Columbia":"CYXS",
    "Québec/Jean Lesage International, Quebec":"CYQB",
    "Red Deer Regional, Alberta":"CYQF",
    "Regina International, Saskatchewan":"CYQR",
    "Saskatoon/John G. Diefenbaker International, Saskatchewan":"CYXE",
    "Sault Ste. Marie, Ontario":"CYAM",
    "Sept-Îles, Quebec":"CYZV",
    "St-Jean, Quebec":"CYJN",
    "St. John's International, Newfoundland and Labrador":"CYYT",
    "Sudbury, Ontario":"CYSB",
    "Thunder Bay, Ontario":"CYQT",
    "Toronto/Billy Bishop Toronto City, Ontario":"CYTZ",
    "Toronto/Buttonville Municipal, Ontario":"CYKZ",
    "Toronto/Lester B. Pearson International, Ontario":"CYYZ",
    "Vancouver Harbour, British Columbia":"CYHC",
    "Vancouver International, British Columbia":"CYVR",
    "Victoria International, British Columbia":"CYYJ",
    "Whitehorse International, Yukon":"CYXY",
    "Windsor, Ontario":"CYQG",
    "Winnipeg/James Armstrong Richardson International, Manitoba":"CYWG",
    "Winnipeg/St. Andrews, Manitoba":"CYAV",
    "Yellowknife, Northwest Territories":"CYZF"
    }

    df = pd.DataFrame(
        list(icao_codes.items()),
        columns=["Airport", "ICAO_OACI"]
    )

    df = df.merge(airport_info, on="ICAO_OACI")
    df.to_csv("../data/airport_icao_codes.csv", index=False)