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
        ], className= "six columns"),
        html.Div([
            dcc.Graph(id="Graph7"),
            dcc.Interval(id="Update_Graph7", interval=50000)
        ], className= "six columns"),
    ]),
    html.Div(className="row", children=[
        html.Div([
            html.Img(src=app.get_asset_url("WordCloud4.png"), style={'height':'90%', 'width':'100%'})
        ], className="six columns"),
        html.Div([
            html.Img(src=app.get_asset_url("WordCloud5.png"), style={'height':'100%', 'width':'80%'})
        ], className="six columns")   
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
        ],className= "one columns"),
        html.Div([
            html.Pre(id="cheat-data")
        ],className= "one columns")
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

@app.callback(Output("click-data7", "children"),
            [Input("Graph7", "clickData")])
def click7(clickData):
    counter = 7
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

@app.callback(Output("cheat-data", "children"),
            [Input("show-forbidden", "n_clicks")])
def cheat_click(clickData):
    counter = 8
    if clickData == None:
        raise PreventUpdate
    else:
        return counter

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

'''
@app.callback(Output("Graph7", "figure"), [Input("Update_Graph7", "n_intervals")])
def update_graph7(input_data):
    #words = ['征信', '拍拍贷', '查询', '报告', '贷款', '个人', '怎么', '信用卡', '逾期', '被拒', '如何', '中心', '信用', '网贷', '人人', '分期', '注册', '好信', '手机', '钱包', '个人信用', '借呗', '平安', '捷信', '微粒贷', '借钱', '记录', '用钱', '可以', '花呗', '身份证', '拍拍', '现金', '微信', '还款', '问问', '产品', '51', '信而富', '什么', '黑名单', '360', '17', '黑户', '怎么办', '金融', '帮你贷', '消除', '密码', '账号', '怎样', '分期乐', '拒绝', '申请']
    words = list(Graph7_Data.keys())
    frequency = list(Graph7_Data.values())

    #frequency = [1083, 393, 353, 167, 123, 119, 83, 64, 57, 46, 44, 40, 37, 31, 29, 29, 28, 26, 25, 23, 23, 22, 21, 19, 18, 18, 18, 18, 18, 17, 15, 15, 15, 15, 14, 14, 13, 13, 13, 13, 13, 13, 12, 12, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10]

    lower, upper = 15, 70
    frequency = [((x - min(frequency)) / (max(frequency) - min(frequency))) * (upper - lower) + lower for x in frequency]


    percent = list(Graph7_Data.values()) #[0.362086258776329, 0.13139418254764293, 0.11802072885322636, 0.055834169174189235, 0.041123370110330994, 0.03978602474088933, 0.02774991641591441, 0.02139752591106653, 0.01905717151454363, 0.015379471748579069, 0.01471079906385824, 0.013373453694416584, 0.012370444667335341, 0.010364426613172852, 0.009695753928452023, 0.009695753928452023, 0.009361417586091608, 0.008692744901370779, 0.008358408559010365, 0.0076897358742895345, 0.0076897358742895345, 0.00735539953192912, 0.007021063189568706, 0.006352390504847877, 0.006018054162487462, 0.006018054162487462, 0.006018054162487462, 0.006018054162487462, 0.006018054162487462, 0.0056837178201270475, 0.005015045135406218, 0.005015045135406218, 0.005015045135406218, 0.005015045135406218, 0.004680708793045804, 0.004680708793045804, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.0043463724506853894, 0.004012036108324975, 0.004012036108324975, 0.00367769976596456, 0.00367769976596456, 0.00367769976596456, 0.00367769976596456, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146, 0.003343363423604146]

    lenth = len(words)
    colors = [py.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(lenth)]

    data = go.Scatter(
        x=list(range(lenth)),
        y=random.choices(range(lenth), k=lenth),
        mode='text',
        text=words,
        #hovertext=['{0}{1}{2}'.format(w, f, format(p, '.2%')) for w, f, p in zip(words, frequency, percent)],
        #hoverinfo='text',
        textfont={'size': frequency, 'color': colors})
    
    layout = {
        "xaxis": {"showgrid": False, 'showticklabels': False, 'zeroline': False},
        "yaxis": {'showgrid': False, 'showticklabels': False, 'zeroline': False}
    }

    return {"data": [data], "layout": layout}
'''

'''
@app.callback(Output("Graph7", "figure"), [Input("Update_Graph7", "n_intervals")])
def update_graph7(input_data):
    wc = WordCloud(stopwords = set(STOPWORDS),
                   max_words = 200,
                   max_font_size = 100)
    wc.generate_from_frequencies(Graph7_Data)
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',  
                       text=word_list
                      )
    
    layout = {
            'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
            'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}
        }
    
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig
'''

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