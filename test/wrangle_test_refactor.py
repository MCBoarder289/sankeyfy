

# TODO: Create Default NULL behavior as an option (Fill with an "unknown" category that you can feed the value for)
# TODO: Make this more like a package/function
# TODO: Account for summary rows/raw rows, and the option to process either in the function


import pandas as pd
import numpy as np
import plotly.offline as py

df = pd.read_csv('./test/data/raw_duped_categories.csv')

# Use List of Columns to Determine the unique Labels

# NOTE: Order Matters, and Hanging Nodes will push to the end
# DOUBLE NOTE: Nulls are taken care of automatically in the looping. (source_target_df is dropping NA references)
# If a bunch are going nowhere, they aren't included anywhere. Might want to handle NA's and replace them with "?"?
# Maybe make the above an option... See raw_duped_categories_nulls2.csv


def sankeyfy(df, agg_col, columns=None, agg='summary'):

    """

    sankeyfy takes a dataframe and puts it into a simple format for Plotly Sankey visualizations

    Params:

        df = Dataframe of your categorical variables, and a single field for counts

        columns = List of columns, and order matters. The visual will <mostly> follow this order.

        agg_col = Column name that is the aggregation column (either unique identifier, or pre-aggregated count).

        agg = Value should be "summary" or "raw". This will determine whether or not
        the function will do a distinct count of your numeric count field ("raw"), or if it needs to
        simply sum up the already pre-aggregated counts ("summary")

    Output:

        Two Pandas dataframes "label" and "source_target_df"

        "label" represents the distinct values for all of the sankey nodes (all of the categorical variables)

        "source_target_df" represents the tall table of all the various flows between the nodes.

    """

    assert isinstance(df, pd.DataFrame), "ERROR: df parameter is not a Pandas dataframe"
    if columns:
        assert isinstance(columns, (list,)), "ERROR: columns parameter is not a list"
        assert len(columns) > 1, "ERROR: columns parameter does not have more than one item"
    assert isinstance(agg_col, str), "ERROR: agg_col parameter is not a string"
    assert (agg == 'summary' or agg == 'raw'), "ERROR: agg parameter needs to be 'summary' or 'raw'"

    # Place unique column values in "label" dataframe
    label = pd.DataFrame(columns=['label', 'field'])

    if not columns:
        # Create a list of columns and removes the agg_col

        columns = df.columns.values.tolist()

        columns.remove(agg_col)

    for column in columns:

        unique_vals = df[column].unique().tolist()
        field_col = [column for _ in range(len(unique_vals))]
        append_df = pd.DataFrame(np.column_stack([unique_vals, field_col]), columns=['label', 'field'])
        label = label.append(append_df)

    label = label.reset_index(drop=True)
    label = label.rename(index=str, columns={0: 'label'})
    label['index'] = label.index

    # Create Source to Target Dataframe

    source_target_df = pd.DataFrame(columns=['source', 'target', 'value'])

    if agg == 'raw':

        for i, j in zip(columns[::1], columns[1::1]):

            grouped_df = df.groupby([i, j], as_index=False)[agg_col].agg({agg_col: 'nunique'})
            rename = grouped_df.merge(label[label['field'] == i], left_on=i, right_on='label', how='left')
            rename[i] = rename['index']
            rename = rename.drop(columns=['label', 'field', 'index'])
            rename = rename.merge(label[label['field'] == j], left_on=j, right_on='label', how='left')
            rename[j] = rename['index']
            rename = rename.drop(columns=['label', 'field', 'index'])

            rename.columns = source_target_df.columns
            source_target_df = source_target_df.append(rename)

    if agg == 'summary':

        for i, j in zip(columns[::1], columns[1::1]):
            grouped_df = df.groupby([i, j], as_index=False)[agg_col].agg({agg_col: 'sum'})
            rename = grouped_df.merge(label[label['field'] == i], left_on=i, right_on='label', how='left')
            rename[i] = rename['index']
            rename = rename.drop(columns=['label', 'field', 'index'])
            rename = rename.merge(label[label['field'] == j], left_on=j, right_on='label', how='left')
            rename[j] = rename['index']
            rename = rename.drop(columns=['label', 'field', 'index'])

            rename.columns = source_target_df.columns
            source_target_df = source_target_df.append(rename)

    return label, source_target_df


columns = ['Cat1', 'Cat2', 'Cat3', 'Cat4']

id_field = 'ID Number'


# Final dfs
#label, final_df = sankeyfy(df, id_field, columns)

label, final_df = sankeyfy(df, id_field)


# Plotly Sankey Trial

data_trace = dict(
    type='sankey',
    domain = dict(
      x =  [0,1],
      y =  [0,1]
    ),
    orientation = "h",
    valueformat = ".0f",
    node = dict(
      pad = 10,
      thickness = 30,
      line = dict(
        color = "black",
        width = 0.5
      ),
      label =  label['label']#,
      #color = "blue"
    ),
    link = dict(
      source = final_df['source'],
      target = final_df['target'],
      value = final_df['value'],
  )
)

layout =  dict(
    title = "Sankey Data Wrangling Test",
    height = 772,
    width = 1118,
    font = dict(
      size = 10
    ),
    updatemenus=[
        dict(
            y=1,
            buttons=[
                dict(
                    label='Light',
                    method='relayout',
                    args=['paper_bgcolor', 'white']
                ),
                dict(
                    label='Dark',
                    method='relayout',
                    args=['paper_bgcolor', 'white']
                )
            ]

        ),
        dict(
            y=0.9,
            buttons=[
                dict(
                    label='Thick',
                    method='restyle',
                    args=['nodethickness', 15]
                ),
                dict(
                    label='Thick',
                    method='restyle',
                    args=['nodethickness', 15]
                )
            ]
        ),
        dict(
            y=0.8,
            buttons=[
                dict(
                    label='Small gap',
                    method='restyle',
                    args=['nodepad', 15]
                ),
                dict(
                    label='Large gap',
                    method='restyle',
                    args=['nodepad', 20]
                )
            ]
        ),
        dict(
            y=0.7,
            buttons=[
                dict(
                    label='Snap',
                    method='restyle',
                    args=['arrangement', 'snap']
                ),
                dict(
                    label='Perpendicular',
                    method='restyle',
                    args=['arrangement', 'perpendicular']
                ),
                dict(
                    label='Freeform',
                    method='restyle',
                    args=['arrangement', 'freeform']
                ),
                dict(
                    label='Fixed',
                    method='restyle',
                    args=['arrangement', 'fixed']
                )
            ]
        ),
        dict(
            y=0.6,
            buttons=[
                dict(
                    label='Horizontal',
                    method='restyle',
                    args=['orientation', 'h']
                ),
                dict(
                    label='Vertical',
                    method='restyle',
                    args=['orientation', 'v']
                )
            ]

        )
    ]
)

fig = dict(data=[data_trace], layout=layout)
py.plot(fig, validate=False)