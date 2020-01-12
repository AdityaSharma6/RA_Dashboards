import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly as py
import random
import plotly.graph_objs as go
import json
from Algorithms import dictionary_dimension_conversion
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
        html.Button("Click here to show the correct answer of your analysis.", id="show-forbidden"),
        html.Div(id="user_answer")
    ]),
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
        ], className= "six columns")#,
        #html.Div([
        #    dcc.Graph(id="Graph7"),
        #    dcc.Interval(id="Update_Graph7", interval=50000)
        #], className= "six columns"),
    ]),
    html.Div(className="row", children=[
        html.Button("Click here to conclude your analysis & generate your survey token.", id="show-secret"),
        html.Div(id="user_results")
    ]),
    html.Div(className = "row", children=[
        html.Div([
            html.Pre(id='click-data1')
        ],className= "one columns"),
        html.Div([
            html.Pre(id="click-data2")
        ],className= "one columns"),
        html.Div([
            html.Pre(id="click-data3")
        ],className= "one columns"),
        html.Div([
            html.Pre(id="click-data4")
        ],className= "one columns"),
        html.Div([
            html.Pre(id="click-data5")
        ],className= "one columns"),
        html.Div([
            html.Pre(id="click-data6")
        ],className= "one columns"),
        html.Div([
            html.Pre(id="click-data7")
        ],className= "one columns")
    ])
])

@app.callback(Output('Graph1', 'figure'), [Input('Update_Graph1', 'n_intervals')])
def update_graph1(input_data):
    revenue_values = Graph1_Data.get("Revenue Values")

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
@app.callback(Output("Graph7", "figure"), [Input("Update_Graph7", "n_intervals")])
def update_graph7(input_data):
    algo = dictionary_dimension_conversion(Graph8_Data)
    dictionary_1 = algo.dict_conversion()
    total = algo.dict_total()

    labels2 = ["Total"]
    parents2 = [""]
    values2 = [total]

    for key, value in dictionary_1.items():
        labels2.append(key)
        parents2.append("Total")
        values2.append(value)

        label_extension = list(Graph8_Data.get(key).keys())

        product_line = key + " "
        product_line_list = ((product_line * len(label_extension)).split(" "))
        product_line_list.pop()
        parents_extension = product_line_list

        values_extension = list(Graph8_Data.get(key).values())

        labels2.extend(label_extension)
        parents2.extend(parents_extension)
        values2.extend(values_extension)

    data = go.Sunburst(
            labels=labels2,
            parents=parents2,
            values=values2,
            branchvalues="total",
            maxdepth=2
        )
    
    layout = {
        "title": "Popular Sentiments of each Product Line",
        "margin": {"l": 20, "t":30, "b":20, "r":20},
        "clickmode": "event+select"
    }

    return {"data": [data], "layout": layout}
'''
@app.callback(Output("click-data1", "children"),
            [Input("Graph1", "clickData")])
def click1(clickData):
    counter = 1
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

@app.callback(Output("click-data2", "children"),
            [Input("Graph2", "clickData")])
def click2(clickData):
    counter = 2
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

@app.callback(Output("click-data3", "children"),
            [Input("Graph3", "clickData")])
def click3(clickData):
    counter = 3
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

@app.callback(Output("click-data4", "children"),
            [Input("Graph4", "clickData")])
def click4(clickData):
    counter = 4
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

@app.callback(Output("click-data5", "children"),
            [Input("Graph5", "clickData")])
def click5(clickData):
    counter = 5
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

@app.callback(Output("click-data6", "children"),
            [Input("Graph6", "clickData")])
def click6(clickData):
    counter = 6
    if clickData == None:
        raise PreventUpdate
    else:
        return counter
'''
@app.callback(Output("click-data7", "children"),
            [Input("Graph7", "clickData")])
def click7(clickData):
    counter = 7
    if clickData == None:
        raise PreventUpdate
    else:
        return counter
'''
@app.callback(Output("user_results", "children"), [Input("show-secret", "n_clicks")])
def secret_key(n_clicks):
    if n_clicks == None:
        raise PreventUpdate
    else:
        return "Scroll down to retrieve your token. Input the token into your Dashboard Account."

@app.callback(Output("user_answer", "children"), [Input("show-forbidden", "n_clicks")])
def secret_key(n_clicks):
    if n_clicks == None:
        raise PreventUpdate
    else:
        return "Jeans USA"


if __name__ == "__main__":
    app.run_server(debug=True)

