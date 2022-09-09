#from tkinter.ttk import Style
from dash import html, dcc
import dash_bootstrap_components as dbc
#from app2 import app

list_of_locations = {

    "All": 0,
    "Manhattan": 1,
    "Bronx": 2,
    "Brooklyn": 3,
    "Queens": 4,
    "Staten Island": 5
}

slider_size = [100,500,100,10000,1000000]

controllers = dbc.Row([
 
  
  html.H3("Vendas de Imóveis - NYC", style = {"margin-top": "30px"}),
  html.P("""Utilize este dashboard para analisar vendas ocorridas na cidade de Nova Yorkno período de 1 ano"""),

   html.H5("""Distrito""", style= {"margin-bottom": "25px", "margin-top" : "50px"}),

   dcc.Dropdown(
    id="location-dropdown",
    options=[{"label": i, "value": j} for i, j in list_of_locations.items()],
    value= 0,
    placeholder= "Selecione o Distrito Desejado"
  
   ),
   html.H5("""Metragem (m2)""", style= { "margin-top" : "20px"}),


   dcc.Slider(min=0,max=4, id="slide-square-size",
    marks={ i: str(j) for i, j in enumerate(slider_size)}),

    html.H5("""Variavél de Controle""", style= { "margin-top" : "20px"}),
    
    dcc.Dropdown(
                options=[
                    {'label': 'Ano de Construção', 'value': 'YEAR BUILT'},
                    {'label': 'Unidade Totais', 'value': 'TOTAL UNITS'},
                    {'label': 'Preço de Venda', 'value': 'SALE PRICE'},

                    ],
                    value= 'SALE PRICE', 
                    id="dropdown_color")

])
