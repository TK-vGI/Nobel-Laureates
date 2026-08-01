"""
AI improved code for stage 5 and stage 6

hs-test-python 11.0.32 requirements:
pandas --version: 2.3.3 (can use df.method(values, inplace=True) without error)
matplotlib --version 3.10.8
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', 8)

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

dfLaureatesDict = dfLaureates[['country', 'name']][:20]
# print(dfLaureatesDict.to_dict())

dfLaureates.dropna(subset=['gender'], inplace=True)
dfLaureates.reset_index(drop=True, inplace=True)

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


# Convert empty strings to NaN
dfLaureates['born_in'].replace("", pd.NA, inplace=True)

# Only update rows where born_in is NaN AND place_of_birth contains a comma
mask = dfLaureates['born_in'].isna() & dfLaureates['place_of_birth'].str.contains(',', na=False)

dfLaureates.loc[mask, 'born_in'] = (
    dfLaureates.loc[mask, 'place_of_birth'].apply(extract_country)
)

# print(dfLaureates.shape)
# dfLaureates.head(20)

dfLaureates.dropna(axis=0, subset=['born_in'], inplace=True)  # 2
dfLaureates.reset_index(drop=True, inplace=True)  # 3

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
dfLaureates[cols] = dfLaureates[cols].replace(country_map)  # 4

list_places = dfLaureates['born_in'].to_list()
# print(len(list_places))
# print(list_places) # 5

"""
3/6: Correct the dates
    1. Generate a new column "year_born", representing the year each Nobel Laureate was born.
    2. Create a new column " age_of_winning", representing the age of winning the prize.
    3. Output two lists — the year of birth column values and the age of obtaining the prize column values,
       separated by a new line character ("\n")
"""
# Convert mixed-format dates
dfLaureates['date_of_birth'] = pd.to_datetime(dfLaureates['date_of_birth'], format="mixed")

# Extract birth year
dfLaureates['year_born'] = dfLaureates['date_of_birth'].dt.year

# Compute age at winning
dfLaureates['age_of_winning'] = dfLaureates['year'] - dfLaureates['year_born']

# Output lists
# print(dfLaureates['year_born'].to_list(),
#       dfLaureates['age_of_winning'].to_list(),
#       sep='\n')

"""
4/6: Plot a pie chart
    1. Re-code the countries to "Other countries" is less than 25 laureates
    2. Format Figure:
        figure size: (12, 12)
        colors: blue, orange, red, yellow, green, pink, brown, cyan, purple
        explode: 0.08
        text displayed on the slices: {:.2f}%\n({:.0f})
    3. Show figure
"""
counts = dfLaureates['born_in'].value_counts()
rare = counts[counts < 25].index

dfLaureates['born_in'] = dfLaureates['born_in'].replace(rare, 'Other countries')

data = dfLaureates['born_in'].value_counts()
labels = data.index
sizes = data.values

colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
explode = [0.00 if i < 3 else 0.08 for i in range(len(labels))]


def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)


plt.figure(figsize=(12, 12))

plt.pie(sizes,
        labels=labels,
        colors=colors[:len(labels)],
        explode=explode,
        autopct=lambda pct: func(pct, data),
        textprops={'color': 'black'}, )

# plt.title('Nobel Laureates by Country of Birth')
plt.show()

"""
5/6: Plot a bar plot
    1. Drop rows where the category column is empty
    2. Format Figure:
        figure size: (10, 10)
        width: 0.4
        gap: 0.2
        colors: blue, crimson
        axis font size: 14
        plot font size: 20
    3. Show figure
    
    AI: Key improvements
        - Use `groupby` instead of `value_counts().sort_index()` repeated three times: One `groupby` gives both male and  
          female counts → no repeated filtering
        - Avoid selecting `[['category']]` (unnecessary): No unnecessary .loc[...] or [['category']] slicing
        - Build a single table of male/female counts → cleaner and safer
        - Use variables with clearer names: Variable names (categories, males, females) are clearer
        - Reduce repeated `.sort_index()` calls: `sort_index()` applied once
        - Make the plotting section more compact
"""
# 1. Drop empty categories
dfLaureates['category'] = dfLaureates['category'].str.strip()
dfLaureates = dfLaureates[dfLaureates['category'] != ""]

# 2. Count males and females per category
gender_counts = (
    dfLaureates.groupby(['category', 'gender'])
    .size() # Compute group sizes
    .unstack(fill_value=0) # Changes groups to columns, use 0 when replacing NaN values
    .sort_index()
)

categories = gender_counts.index.to_list()
males = gender_counts['male'].to_list()
females = gender_counts['female'].to_list()

# 3. Plot
x = np.arange(len(categories))

plt.figure(figsize=(10, 10))

plt.bar(x - 0.2, males, width=0.4, color='blue', label='Males')
plt.bar(x + 0.2, females, width=0.4, color='crimson', label='Females')

# """
# You can eliminate the intermediate lists entirely,
# But the version above is already very readable.
# """
# plt.bar(x - 0.2, gender_counts['male'], width=0.4, color='blue')
# plt.bar(x + 0.2, gender_counts['female'], width=0.4, color='crimson')

plt.xticks(x, categories)
plt.xlabel('Category', fontsize=14)
plt.ylabel('Nobel Laureates Count', fontsize=14)
plt.title('The total count of male and female Nobel Prize winners by categories', fontsize=20)
plt.legend(loc='upper right')

plt.show()

"""
5/6: Plot a bar plot
    1. Drop rows where the category column is empty
    2. Format Figure:
        figure size: (10, 10)
        width: 0.4
        gap: 0.2
        colors: blue, crimson
        axis font size: 14
        plot font size: 20
    3. Show figure
    
    AI: Key improvements
        - Clean list comprehension: No manual loop with indexing, no repeated `.loc[...]` boilerplate
        - No unnecessary `np.array(...)', '.values` already returns a NumPy array. Wrapping it again is redundant.
        - No duplicated category names in `category = [...]` and `tick_labels = [...]`
        - Make the plotting section more compact
"""
# Categories in sorted order (same as tester expects)
categories = ['Chemistry', 'Economics', 'Literature', 'Peace', 'Physics', 'Physiology or Medicine']

# Collect age distributions per category
data = [dfLaureates.loc[dfLaureates['category'] == cat, 'age_of_winning'].values
        for cat in categories]

# """
# Optional readability upgrade: build the data using `groupby()`
# """
# grouped = dfLaureates.groupby('category')['age_of_winning']
# data = [grouped.get_group(cat).values for cat in categories]
# data.append(dfLaureates['age_of_winning'].values)

# Add "All categories" distribution
data.append(dfLaureates['age_of_winning'].values)

tick_labels = categories + ['All categories']

plt.figure(figsize=(10, 10))

plt.boxplot(
    data,
    tick_labels=tick_labels,
    medianprops={'color': 'orange'},
    showmeans=True,
    meanprops={'markerfacecolor': 'green', 'markeredgecolor': 'green'}
)

plt.ylabel('Age of Obtaining the Nobel Prize', fontsize=14)
plt.xlabel('Category', fontsize=14)
plt.title('Distribution of Ages by Category', fontsize=20)

plt.show()