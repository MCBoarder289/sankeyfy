


import pandas as pd
import plotly.offline as py
from sankeyfy import sankeyfy

df = pd.read_csv('./test/data/summary_duped_categories.csv')


column_names = ['Cat1', 'Cat2', 'Cat3', 'Cat4']

id_field = 'ID Number'


# Final dfs
#label_df, final_df = sankeyfy(df, id_field, column_names)

#label_df, final_df = sankeyfy(df, id_field)


#label_df, final_df = sankeyfy(df, agg_col='Count', agg='summary')

label_df, final_df = sankeyfy(df, agg_col='Count', columns=column_names, agg='summary')


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
      label =  label_df['label']#,
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