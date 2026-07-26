import pandas as pd

pd.set_option('display.max_columns', 8)

if __name__ == "__main__":
    df = pd.read_json('data/nobel_laureates.json')

    # print(df.axes)
    # print(df.shape)
    # print(df.info())
    # print(df.isna().sum())

    duplicates = df.duplicated(keep=False).sum()
    print('True' if duplicates != 0 else 'False')

    df.dropna(subset=['gender'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    dfDict = df[['country', 'name']][:20]
    print(dfDict.to_dict())