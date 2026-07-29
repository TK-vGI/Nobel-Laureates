# Stage 3/6: Correct the dates
## Description
In this stage, you need to further work on the data. As you may notice, the DataFrame contains the date of birth and  
the year of getting the Nobel Prize. Using this information, you can deduce a new feature — at which age a laureate got  
the Nobel Prize.

## Objectives
Calculate the age when a laureate received the Nobel Prize. Use the information present in the dataset to get it.
1. The dates of birth are present in 4 formats: `26 April 1932`, `1951-3-26`, `December 13, 1923`, and, `1950`. Generate a new column,  
   representing the year each Nobel Laureate was born.
2. Create a new column, representing the age of winning the prize. It is the year of winning the prize minus the year of birth.

As a result of this stage, output two lists — the year of birth column values and the age of obtaining the prize column values,  
separated by a new line character (`"\n"`). Use the `.to_list()` method of Series.

## Example
### Example 1:
_Note that most columns and rows in the example are omitted._

_Initial data:_

```
         date_of_birth  year
0       8 October 1927  1984
1       9 October 1892  1961
2        July 23, 1906  1975
3         26 July 1829  1909
4       29 August 1862  1911
5           1948-11-26  2009
```

_Resulting DataFrame:_

```
         date_of_birth  year  year_born  age_of_winning
0       8 October 1927  1984       1927              57
1       9 October 1892  1961       1892              69
2        July 23, 1906  1975       1906              69
3         26 July 1829  1909       1829              80
4       29 August 1862  1911       1862              49
5           1948-11-26  2009       1948              61
```

_Output:_
```
[1927, 1892, 1906, 1829, 1862, 1948]
[57, 69, 69, 80, 49, 31]
```