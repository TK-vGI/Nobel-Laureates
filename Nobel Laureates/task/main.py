import pandas as pd

pd.set_option('display.max_columns', 8)

if __name__ == "__main__":
    """
    1/6: Load the dataset from the JSON file.
        1. Explore the data and check
        2. Check for duplicates
        3. Drop NaN rows in 'gender' column
        5. Reset index dataframe
    """
    dfLaureates = pd.read_json('data/nobel_laureates.json')

    # print(dfLaureates.axes)
    # print(dfLaureates.shape)
    # print(dfLaureates.info())
    # print(dfLaureates.isna().sum())

    duplicates = dfLaureates.duplicated(keep=False).sum()
    # print('True' if duplicates != 0 else 'False')

    dfLaureates.dropna(subset=['gender'], inplace=True)
    dfLaureates.reset_index(drop=True, inplace=True)

    dfLaureatesDict = dfLaureates[['country', 'name']][:20]
    # print(dfLaureatesDict.to_dict())

    """
    2/6: Correct the birthplaces
        1. Extract the country names from the place_of_birth column and fill them to 'born_in' column
        2. Drop NaN rows in 'born_in' column
        3. Reset index dataframe
        4. Modify the names of countries
        5. Output a list of born_in column values
    """
    def extract_country(place):
        if not place:
            return None
        parts = place.split(',')
        return parts[-1].strip() if len(parts) > 1 else None

    dfLaureates['born_in'] = dfLaureates['place_of_birth'].apply(extract_country) # 1
    # print(dfLaureates.shape)
    # dfLaureates.head(20)

    dfLaureates.dropna(axis=0,subset=['born_in'],inplace=True) # 2
    dfLaureates.reset_index(drop=True, inplace=True) # 3

    country_map = {
        "US": "USA",
        " U.S.": "USA",
        "U.S.": "USA",
        " United States": "USA",
        "United States": "USA",

        " United Kingdom": "UK",
        "United Kingdom": "UK"
    }

    cols = ['born_in', 'country', 'place_of_birth', 'place_of_death']
    dfLaureates[cols] = dfLaureates[cols].apply(lambda s: s.str.strip())
    dfLaureates[cols] = dfLaureates[cols].replace(country_map) #4

    list_born_in = dfLaureates['born_in'].to_list() #5
    print(list_born_in) # 5