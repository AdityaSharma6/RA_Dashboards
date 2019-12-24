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
click_counter = []
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
            dcc.Interval(id="Update_Graph3", interval=12000)
        ],className="six columns"),
        html.Div([
            dcc.Graph(id="Graph6"),
            dcc.Interval(id="Update_Graph6", interval=14000)
        ],className= "six columns")
    ]),


    html.Div(className="row", children=[
        html.Div([
            dcc.Graph(id="Graph5"),
            dcc.Interval(id="Update_Graph5", interval=16000)
        ], className= "six columns"),
        html.Button("Click here to conclude your analysis & generate your survey token.", id="show-secret"),
        html.Div(id="user_results")
        #html.Div([
        #    dcc.Graph(id="Graph8"),
        #    dcc.Interval(id="Update_Graph8", interval=16000)
        #], className= "six columns")
    ]),
    html.Div(children=[
        html.Pre(id='click-data1'),
        html.Pre(id="click-data2"),
        html.Pre(id="click-data3"),
        html.Pre(id="click-data4"),
        html.Pre(id="click-data5"),
        html.Pre(id="click-data6")
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
        "title": "Sum of Revenue per Country (USD)",
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
        hoverinfo = 'label+percent+value',
        #hovertemplate= 'Cost: $%{y_values}<br>Product Line: %{hovertext}'
    )

    layout = {
        "title": "Sum of Revenue per Product Line (USD)",
        "clickmode": "event+select"
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
        "title": "Sum of Profit per Product Line per Channel (USD)",
        "barmode": "group",
        "bargap": 0.5,
        "clickmode": "event+select"
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
        "title": "Sum of Product Cost per Country (USD)",
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

    layout = {
        "title": "Sum of Product Cost per Product Line (USD)",
        "clickmode": "event+select"
    }

    return {"data": [data], "layout": layout}



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
        "title": "Sum of Product Cost per Product Line per Channel (USD)",
        "barmode": "group",
        "bargap": 0.5,
        "xaxis_title": "Product Per Channel",
        "yaxis_title": "Cost in USD",
        "clickmode": "event+select"
    }

    return {"data": [data_dm, data_rt, data_em], "layout": layout}

'''
@app.callback(Output("Graph8", "figure"), [Input("Update_Graph8", "n_intervals")])
def update_graph8(input_data):
    levels = ["Comments", "Product Line"]
    parents = list(Graph8_Data.keys())
    labels = list(Graph8_Data.get("Dresses").keys())
    final_values = [] 
    final_labels = []
    for i in range(len(parents)):
        final_labels.append(parents[i])
        for j in range(len(labels)):
            final_labels.append(labels[i])
            final_values.extend(list(list(Graph8_Data.values())[i].values()))

    
    data = go.Sunburst(
        labels=["Nirmal", "Archana", "Aditya", "Poonam", "Noor", "Tulsi"],
        parents=["Nirmal", "Archana"],
        values=[52, 50, 19, 15, 13, 6],
        branchvalues="total"
    )

    return {"data": [data]}
'''

@app.callback(Output("click-data1", "children"),
            [Input("Graph1", "clickData")])
def click1(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        click_counter.append(1)
        raise PreventUpdate

@app.callback(Output("click-data2", "children"),
            [Input("Graph2", "clickData")])
def click2(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        click_counter.append(2)
        raise PreventUpdate

@app.callback(Output("click-data3", "children"),
            [Input("Graph3", "clickData")])
def click3(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        click_counter.append(3)
        raise PreventUpdate

@app.callback(Output("click-data4", "children"),
            [Input("Graph4", "clickData")])
def click4(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        click_counter.append(4)
        raise PreventUpdate

@app.callback(Output("click-data5", "children"),
            [Input("Graph5", "clickData")])
def click5(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        click_counter.append(5)
        raise PreventUpdate

@app.callback(Output("click-data6", "children"),
            [Input("Graph6", "clickData")])
def click6(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        click_counter.append(6)
        raise PreventUpdate

@app.callback(Output("user_results", "children"), [Input("show-secret", "n_clicks")])
def secret_key(n_clicks):
    if n_clicks == None:
        raise PreventUpdate
    else:
        number = generate_number(click_counter)
        click_counter = []
        return (f"{number}")

def generate_number(click_counter):
    if click_counter == []:
        return 789
    click_counter = list(set(click_counter))
    number = 0
    for i in range(len(click_counter)):
        value = click_counter[i]
        number = number * 10
        number += value

    click_counter = []
    return number


if __name__ == "__main__":
    app.run_server(debug=True)