# Stage 2/6: Correct the birthplaces
## Description
The data is very heterogeneous. Let's correct it! As you can see, two columns contain information on the Nobel laureates'  
places of birth, aggregate the information into one column.

## Objectives
Some values in the `born_in` column are missing. Correct them with the `place_of_birth` column values.
1. Extract the country names from the `place_of_birth` column. Typically, this column contains the name of the city and,  
   sometimes, state and country of birth. The values are separated by a comma. To extract the country, split each column  
   value by comma (if it is present) and take the last value. Apply `.strip()` to the Python string to remove the excessive  
    white spaces. If no comma is present in the column value, replace the value with `None`;
2. Fill the `born_in` empty values with the new values of the `place_of_birth` column. If the `born_in` column still contains  
   empty values, drop the respective rows. `Reset` the DataFrame index;
3. Modify the names of countries — replace `US`, `United States`, and `U.S.` with `USA`, and `United Kingdom` with `UK`.

As a result, output a list of `born_in` column values.

## Example
### Example 1:
_Note that most columns and rows in the example are omitted._

_Initial DataFrame:_
```
                     born_in                       place_of_birth
0                                       Bahía Blanca ,  Argentina
1     Bosnia and Herzegovina   Sarajevo ,  Bosnia and Herzegovina
2                         US
3                                                    Buenos Aires                                  
```

_Resulting DataFrame:_
```
                     born_in                 place_of_birth
0                  Argentina                      Argentina
1     Bosnia and Herzegovina         Bosnia and Herzegovina
2                        USA                                
```

_Output:_
```
['Argentina', 'Bosnia and Herzegovina', 'USA']
```