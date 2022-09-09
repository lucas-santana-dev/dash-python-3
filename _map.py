from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from index import app


fig = go.Figure()

fig.update_layout(template = "ggplot2",paper_bgcolor= "rgba (0,0,0,0)")

map = dbc.Row([

    dcc.Graph(id = "map-graph", figure=fig)
   
],style = ({"height": "80vh"})
)
