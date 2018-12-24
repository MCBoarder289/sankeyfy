
import pandas as pd
import numpy as np


def sankeyfy(df, agg_col, columns=None, agg='summary'):

    """

    sankeyfy takes a dataframe and puts it into a simple format for Plotly Sankey visualizations

    Params:

        df = Dataframe of your categorical variables, and a single field for counts

        columns = List of columns, and order matters. The visual will <mostly> follow this order.
                  Not passing columns naively will filter out your agg_col and use the current order.

        agg_col = Column name that is the aggregation column (either unique identifier, or pre-aggregated count).

        agg = Value should be "summary" or "raw". This will determine whether or not
              function will do a distinct count of your numeric count field ("raw"), or if it needs to
              simply sum up the already pre-aggregated counts ("summary")

    Output:

        Two Pandas dataframes "label" and "source_target_df"

        "label" represents the distinct names for all of the sankey nodes (all of the categorical variables)

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

    for i, j in zip(columns[::1], columns[1::1]):

        if agg == 'raw':
            grouped_df = df.groupby([i, j], as_index=False)[agg_col].agg({agg_col: 'nunique'})

        elif agg == 'summary':
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