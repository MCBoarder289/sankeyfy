# Sankeyfy - Data wrangling for easy Sankey Visualizations

The Sankeyfy package aims to simplify the creation of a Sankey
visualization through a straightforward function call. Simply
run the "sankeyfy" function on your dataframe, and it will output
the necessary dataframes for a Sankey chart.

I built this for specifically for use with the **Plotly**  API,
but this should also be useful for its sources or other D3 libraries.

The function accounts for the following scenarios, and attempts
to leverage sensible default behavior (but feel free to give feedback 
or contribute!):

1. *Default Scenario:* **Pre-aggregated format**
    * Input is a table of categorical variables/columns with a 
    single aggregate column (counts/count distinct, etc.)
    
2. **Raw Format**
    * Input is a raw table where each row is an observation and
    the columns are all categorical variables.
    * Currently assumes there is a unique id field, will add default
    functionality for this later
    
    
Please feel free to give me any feedback or contribute with a PR,
and hopefully this saves your some time trying to build out some cool
Sankey visuals!


## To Do:

1. DONE - Create Default NULL behavior as an option (Fill with an "unknown" category that you can feed the value for)
2. DONE - Build functionality to create an ID field if one isn't provided...

Copyright 2018, MIT License
     

