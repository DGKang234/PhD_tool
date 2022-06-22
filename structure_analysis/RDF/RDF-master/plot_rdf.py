#pip install plotly

import plotly.express as px
import pandas as pd

dff = pd.read_csv('output.csv')
fig = px.line(dff, x=dff.columns[0], y=dff.columns[1], title=None)
fig.show()

