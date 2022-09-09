from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()

fig.update_layout(template = "ggplot2" ,paper_bgcolor= "rgba (0,0,0,0)")

hist = dbc.Row([

    dcc.Graph(id = "hist-graph", figure=fig)
   
],style = ({"height": "20vh"})
)
