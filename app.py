import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server
app.title = "Big Data Dashboard"

app.layout = html.Div([
    html.Div(className="row", children=[
        html.Div([
            dcc.Graph(id='Graph1'),
            dcc.Interval(id="Update_Graph1", interval=200000)
        ],className="four columns"),
        html.Div([
            dcc.Graph(id="Graph4"),
            dcc.Interval(id="Update_Graph4", interval=200000)
        ],className="four columns"),
        html.Div([
            dcc.Graph(id="Graph2"),
            dcc.Interval(id="Update_Graph2", interval=100000)
        ],className= "four columns") #, style={'float': 'right', 'width': '40%'})
    ]), #, style={'float': 'left', 'width': '40%'})


    html.Div(className="row", children=[
        html.Div([
            dcc.Graph(id="Graph3"),
            dcc.Interval(id="Update_Graph3", interval=10000)
        ],className="six columns"),
        html.Div([
            dcc.Graph(id="Graph6"),
            dcc.Interval(id="Update_Graph6", interval=10000)
        ],className= "six columns")
    ]),


    html.Div(className="row", children=[
        html.Div([
            dcc.Graph(id="Graph5"),
            dcc.Interval(id="Update_Graph5", interval=10000)
        ], className= "six columns")
    ]),
    html.Div(children=[
        html.Pre(id='click-data')
        ])
])

@app.callback(Output('Graph1', 'figure'), [Input('Update_Graph1', 'n_intervals')])
def update_graph1(input_data):
    revenue_values = Graph1_Data.get("Revenue Values")

    for i in range(len(revenue_values)):
        random_num = random.uniform(0.8, 1.2)
        revenue_values[i] = random_num * revenue_values[i]

    data = go.Scattergeo(
        name="Revenue",
        showlegend=True,
        mode="markers",
        lat= Graph1_Data.get("Latitude"),
        lon= Graph1_Data.get("Longitude"),
        text= revenue_values,
        hovertext= Graph1_Data.get("Countries"),
        hovertemplate= 'Revenue: $%{text: .0f}<br>Country: %{hovertext}',
        marker= dict(
            opacity=1,
            size= revenue_values,
            sizeref=1000,
            sizemin=1,
            sizemode="area",
            gradient = dict (
                type="radial",
                color="red"
            ),
            color = "blue"
        )
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
        #"margin": {'l': 30, 'r': 30, 'b': 10, 't': 49},
        "clickmode": "event+select"
    }
    return {"data": [data], "layout": layout} 



@app.callback(Output('Graph2', 'figure'), [Input('Update_Graph2', 'n_intervals')])
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



@app.callback(Output("Graph3", "figure"), [Input("Update_Graph3", "n_intervals")])
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
        name="Direct Marketing",

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
        "title": "Product Type by Channel and Profit",
        "barmode": "group",
        "bargap": 0.5
    }

    return {"data": [data_dm, data_rt, data_em], "layout": layout}



@app.callback(Output('Graph4', 'figure'), [Input('Update_Graph4', 'n_intervals')])
def update_graph4(input_data):

    data = go.Scattergeo(
        name="Product Cost",
        showlegend=True,
        mode="markers",
        lat= Graph4_Data.get("Latitude"),
        lon= Graph4_Data.get("Longitude"),
        text= Graph4_Data.get("Product Cost Values"),
        hovertext= Graph4_Data.get("Countries"),
        hovertemplate= "Product Cost: $%{text: .0f}<br>Country: %{hovertext}",
        marker= dict(
            opacity=1,
            size=Graph4_Data.get("Product Cost Values"),
            sizeref=1000,
            sizemin=1,
            sizemode="area",
            gradient = dict (
                type="radial",
                color="red"
            ),
            color = "blue"
        )
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
       # "margin": {'l': 30, 'r': 10, 'b': 10, 't': 49}
       "clickmode": "event+select"
    }
    return {"data": [data], "layout": layout} 
    

    
@app.callback(Output("Graph5", "figure"), [Input("Update_Graph5", "n_intervals")])
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



@app.callback(Output("Graph6", "figure"), [Input("Update_Graph6", "n_intervals")])
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
        "title": "Product Type by Channel and Product Cost",
        "barmode": "group",
        "bargap": 0.5,
        "xaxis_title": "Product Per Channel",
        "yaxis_title": "Cost in USD"
    }

    return {"data": [data_dm, data_rt, data_em], "layout": layout}


@app.callback(Output("click-data", "children"),
            [Input("Graph1", "clickData")])
def display_click_data(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        counter += 1
        return counter

if __name__ == "__main__":
    app.run_server(debug=True)