import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
import json
import os

Graph1 = "country_by_revenue.json"
Graph2 = "product_type_by_revenue.json"
Graph3 = "product_type_by_channel_and_profit.json"
Graph4 = "country_by_product_cost1.json"
Graph5 = "product_type_by_cost.json"
Graph6 = "product_type_by_channel_and_cost.json"
Graph7 = "social_media_comments.json"
Graph8 = "social_media_comments_by_product_line.json"
countries = "countries.json"

with open(countries, "r") as file:
    countries_data = json.load(file)
with open (Graph1, "r") as file:
    Graph1_Data = json.load(file)
with open (Graph2, "r") as file:
    Graph2_Data = json.load(file)
with open (Graph3, "r") as file:
    Graph3_Data = json.load(file)
with open (Graph4, "r") as file:
    Graph4_Data = json.load(file)
with open (Graph5, "r") as file:
    Graph5_Data = json.load(file)
with open (Graph6, "r") as file:
    Graph6_Data = json.load(file)
with open (Graph7, "r") as file:
    Graph7_Data = json.load(file)
with open (Graph8, "r") as file:
    Graph8_Data = json.load(file)

app = dash.Dash(__name__)
server = app.server
app.title = "Big Data Dashboard"
header_text = '''
Welcome to Big Data Dashboard!
Below, you will be presented with a series of Graphs. Use these graphs along with your amazing Data Analyst skills to reach a decisive conclusion.
Best of Luck!
'''
app.layout = html.Div([
    html.Div([
        html.Div([
        dcc.Graph(id='Graph1'),
        dcc.Interval(id="Update_Graph1", interval=20000)
        ]), #, style={'float': 'left', 'width': '40%'})
        html.Div([
            dcc.Graph(id="Graph2"),
            dcc.Interval(id="Update_Graph2", interval=10000)
        ]) #, style={'float': 'right', 'width': '40%'})
    ]),
    html.Div([
        dcc.Graph(id="Graph3"),
        dcc.Interval(id="Update_Graph3", interval=10000)
    ]),
    html.Div([
        dcc.Graph(id="Graph4"),
        dcc.Interval(id="Update_Graph4", interval=10000)
    ]),
    html.Div([
        dcc.Graph(id="Graph5"),
        dcc.Interval(id="Update_Graph5", interval=10000)
    ]),
    html.Div([
        dcc.Graph(id="Graph6"),
        dcc.Interval(id="Update_Graph6", interval=10000)
    ])

])

@app.callback(Output('Graph1', 'figure'),
            [Input('Update_Graph1', 'n_intervals')])
def update_graph1(input_data):
    '''data = {
        "type": "scattergeo",
        "lat": Graph1_Data.get("Latitude"),
        "lon": Graph1_Data.get("Longitude"),
        "text": Graph1_Data.get("Revenue Values"),
        "marker": {
            "color": 25.0,
            "size": "pop",
            "opacity": 1
        } 
    }'''

    data = go.Scattergeo(
        lat= Graph1_Data.get("Latitude"),
        lon= Graph1_Data.get("Longitude"),
        text= Graph1_Data.get("Revenue Values"),
        hovertemplate= 'Revenue: $%{text: .0f}'
    )
    
    layout = {
        "geo": {
            "scope": "world", 
            "showframe": True, 
            "projection": {"type": "orthographic"},  #miller, orthographic, hide
            "showcountries": False, 
            "showcoastlines": True
        }, 
        "title": "Country Revenue",
        "hovermode": "closest",
        "margin": {'l': 30, 'r': 10, 'b': 10, 't': 49}
    }
    return {"data": [data], "layout": layout} 


@app.callback(Output('Graph2', 'figure'),
            [Input('Update_Graph2', 'n_intervals')])
def update_graph2(input_data):
    x_values = list(Graph2_Data.keys())
    y_values = list(Graph2_Data.values())

    for i in range(len(y_values)):
        random_num = random.uniform(0.9, 1.1)
        y_values[i] = int(y_values[i] * random_num)
    
    data = go.Pie(
        labels = x_values,
        values = y_values,
        hoverinfo = 'label+percent+value'
    )

    layout = {
        "title": "Product Line by Cost"
    }

    return {"data": [data], "layout": layout}


@app.callback(Output("Graph3", "figure"),
            [Input("Update_Graph3", "n_intervals")])
def update_graph3(input_data):
    x_values = list(Graph3_Data.get("Retail").keys())
    direct_marketing = list(Graph3_Data.get("Direct Marketing").values())
    ecommerce = list(Graph3_Data.get("Ecommerce").values())
    retail = list(Graph3_Data.get("Retail").values())
    
    for i in range(len(x_values)):
        random_num_dm = random.uniform(0.9, 1.1)
        random_num_em = random.uniform(0.9, 1.1)
        random_num_rt = random.uniform(0.9, 1.1)
        direct_marketing[i] = direct_marketing[i] * random_num_dm
        ecommerce[i] = ecommerce[i] * random_num_em
        retail[i] = retail[i] * random_num_rt
    
    data_dm = go.Bar(
        x = x_values,
        y = direct_marketing,
        name="Direct Marketing"
    )
    data_em = go.Bar(
        x= x_values,
        y= ecommerce,
        name="Ecommerce"
    )
    data_rt = go.Bar(
        x= x_values,
        y= retail,
        name= "Retail"
    )

    layout = {
        "height": 800,
        "width": 1000
    }

    return {"data": [data_dm, data_rt, data_em], "layout": layout}


@app.callback(Output('Graph4', 'figure'),
            [Input('Update_Graph4', 'n_intervals')])
def update_graph4(input_data):

    data = go.Scattergeo(
        lat= Graph4_Data.get("Latitude"),
        lon= Graph4_Data.get("Longitude"),
        text= Graph4_Data.get("Product Cost Values"),
        hovertemplate= 'Product Cost: $%{text: .0f}'
    )
    
    layout = {
        "geo": {
            "scope": "world", 
            "showframe": True, 
            "projection": {"type": "orthographic"},  #miller, orthographic, hide
            "showcountries": False, 
            "showcoastlines": True
        }, 
        "title": "Country Product Cost",
        "hovermode": "closest",
        "margin": {'l': 30, 'r': 10, 'b': 10, 't': 49}
    }
    return {"data": [data], "layout": layout} 
    
    
@app.callback(Output("Graph5", "figure"),
            [Input("Update_Graph5", "n_intervals")])
def update_graph5(input_data):

    x_values = list(Graph5_Data.keys())
    y_values = list(Graph5_Data.values())

    for i in range(len(y_values)):
        random_num = random.uniform(0.9, 1.1)
        y_values[i] = y_values[i] * random_num
    
    data = go.Bar(
        name="Product Type by Cost",
        x= y_values,
        y= x_values,
        orientation="h"
    )

    return {"data": [data]}


@app.callback(Output("Graph6", "figure"),
            [Input("Update_Graph6", "n_intervals")])
def update_graph6(input_data):
    x_values = list(Graph6_Data.get("Direct Marketing").keys())
    direct_marketing = list(Graph6_Data.get("Direct Marketing").values())
    ecommerce = list(Graph6_Data.get("Ecommerce").values())
    retail = list(Graph6_Data.get("Retail").values())

    for i in range(len(x_values)):
        random_num_dm = random.uniform(0.9, 1.1)
        random_num_em = random.uniform(0.9, 1.1)
        random_num_rt = random.uniform(0.9, 1.1)
        direct_marketing[i] = direct_marketing[i] * random_num_dm
        ecommerce[i] = ecommerce[i] * random_num_em
        retail[i] = retail[i] * random_num_rt
    
    data_dm = go.Bar(
        y = x_values,
        x = direct_marketing,
        name="Direct Marketing",
        orientation= "h"
    )
    data_em = go.Bar(
        y= x_values,
        x= ecommerce,
        name="Ecommerce",
        orientation= "h"
    )
    data_rt = go.Bar(
        y= x_values,
        x= retail,
        name= "Retail",
        orientation= "h"
    )
    layout = {
        "height": 800,
        "width": 1000
    }

    return {"data": [data_dm, data_rt, data_em], "layout": layout}



if __name__ == "__main__":
    app.run_server(debug=True)