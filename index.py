from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from _map import *
from _histogram import *
from _controllers import *
import plotly.express as px
import numpy as np
from index import app
import dash
import dash_bootstrap_components as dbc


#=================Data============================#
df_data = pd.read_csv("dataset\cleaned_data.csv", index_col=0)
mean_lat = df_data["LATITUDE"].mean()#Calcular a Latitude Media usando a função mean 
mean_long = df_data["LONGITUDE"].mean()#Calcula a longitude média usando a função mean

df_data["TAMANHO EM METROS QUADRADOS"] = df_data["GROSS SQUARE FEET"] / 10.764 #CONVERTE A UNIDADE DE MEDIDA DE PÉS PARA METRO QUADRADO E COLOCA NO DATAFRAME UMA COLUNA COM ESSE DADO
df_data = df_data[df_data["YEAR BUILT"]> 0]#REMOVE APARTAMENTO QUE NÃO TEM ANO DEFINIDO
df_data["SALE DATE"] = pd.to_datetime(df_data["SALE DATE"])#CONVERTE A INFORMAÇÃO DE DATA QUE ESTAVA COM STRING PARA DATETIME


df_data.loc[df_data["TAMANHO EM METROS QUADRADOS"] > 10000, "TAMANHO EM METROS QUADRADOS"] = 10000
df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000
df_data.loc[df_data["SALE PRICE"] < 10000, "SALE PRICE"] = 10000
#====================Layout========================#



app.layout = dbc.Container(
        children=[

                 dbc.Row([
                        
                        dbc.Col([controllers], md=3),
                        dbc.Col([map, hist ], md=9),


                 ])

        ], fluid=True, )


#==================CALLBACK========================#

@app.callback([Output('hist-graph', 'figure'), Output('map-graph', 'figure')],
        [Input('location-dropdown', 'value'),
         Input('slide-square-size', 'value'),
         Input('dropdown_color', 'value')])


def update_hist(location, square_size, color_map):
        if location is None:
                df_intermediate = df_data.copy()
        else: 
                df_intermediate = df_data[df_data["BOROUGH"] == location] if location != 0 else df_data.copy()

                size_limit = slider_size[square_size] if square_size is not None else df_data["GROSS SQUARE FEET"].max()

                df_intermediate = df_intermediate[df_intermediate["GROSS SQUARE FEET"]<=size_limit]

        hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75) 
        
        hist_layout = go.Layout(
                margin=go.layout.Margin(l=10,r=0,t=0,b=50),
                showlegend=False,
                template="ggplot2",
                paper_bgcolor="rgba(0,0,0,0)")

        hist_fig.layout = hist_layout
        

        px.set_mapbox_access_token(open("keys/mapbox_key").read())
        
        colors_rgb = px.colors.sequential.Blackbody
        df_data[color_map].quantile([0.1,0.2])
        df_quantiles = df_data[color_map].quantile(np.linspace(0, 1, len(colors_rgb))).to_frame()
        df_quantiles = (df_quantiles - df_quantiles.min()) / (df_quantiles.max() - df_quantiles.min())
        df_quantiles["colors"]=colors_rgb
        df_quantiles.set_index(color_map, inplace=True)

        color_scale =[[i,j] for i, j in df_quantiles["colors"].iteritems()]
       


        map_fig = px.scatter_mapbox(df_intermediate, lat="LATITUDE", lon="LONGITUDE", color=color_map,
                size="TAMANHO EM METROS QUADRADOS", size_max=15, zoom=10, opacity = 0.4)
        map_fig.update_coloraxes(colorscale=color_scale)        
        map_fig.update_layout (mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_long)),
        template= "ggplot2", paper_bgcolor="rgba(0,0,0,0)",
        margin=go.layout.Margin(l=10,r=10,t=10,b=10),)

        return hist_fig, map_fig
#====================Server========================#
if __name__ == '__main__':
    
    app.run_server(port=8050, host='0.0.0.0')
    