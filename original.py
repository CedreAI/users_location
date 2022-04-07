# libraries
import pandas
import plotly.express as px
from dash import Dash, html, Input, Output, dcc
from persiantools.jdatetime import JalaliDate
from random import randint
import os

# database
global_df = pandas.read_csv("visitor.tsv", "\t")

# set mor date to database
#         #
#      #  #  # 
#       # # #
#         #
#
# 1:    Convert AD to glory
date = []
for i in global_df["DATE"]:
    date.append(JalaliDate.to_jalali(int(i.split("-")[0]), int(i.split("-")[1]), int(i.split("-")[2])))
global_df["DATE"] = date
#        @
# 2:    Determine the day and date
dh = []
for i in global_df["DATE TIME LOGIN"]:
    dh.append(JalaliDate.to_jalali(int(i.split(" ")[0].split("-")[0]), int(i.split(" ")[0].split("-")[1]), int(i.split(" ")[0].split("-")[2])).isoformat() + " " + i.split(" ")[1].split(":")[0] + ":00")
global_df["DATE TIME"] = dh
#         @
# 3:    To specify a server for each user at random
servers = ["quranic.network", "ebad.quranic.network", "motaghin.quranic.network"]
s_l = []
for i in global_df["IP"]:
    s_l.append(servers[randint(0, 2)])
global_df["SERVER"] = s_l
#         @
# 4:    Set login number
val_log = []
for i in global_df["IP"]:
    val_log.append(1)
global_df["LOGIN NUMBER"] = val_log
#
# set copy datebase
original_df = pandas.DataFrame()
original_df = global_df
#
#
#   #    #  ######  #        #  #########
#   ##   #  #         #   #         #    
#   # #  #  ######      #           #    
#   #  # #  #         #   #         #    
#   #    #  ######  #        #      #    
#
#
#  #       ######  #       #  ######  #     
#  #       #        #     #   #       #     
#  #       ######    #   #    ######  #     
#  #       #          # #     #       #     
#  ######  ######      #      ######  ######
#
#
# work with dash
app = Dash()
# Set live components
#         #
#      #  #  # 
#       # # #
#         #
#
# 1:    Build a days-slicer and change the database with it and update the layouts
dic = {}
for i in original_df["DATE"]:
    dic[i] = 0
days_list = list(dic.keys()) # We need the list of days in the days slicer
# >>>   Output for days-slicer
@app.callback(
    Output("output_slicer", "children"),
    Input("input_slicer", "value")
)
def output_slicer(value):
    values = days_list
    v_in = values[value[0]:value[1]+1]
    return f"[{v_in[0]}, {v_in[-1]}]"
# >>>   update database adn return select_server function
server = "all" # This component is required to keep up with server changes and is "all" by default
@app.callback(
    Output("return_select_server", "children"),
    Input("input_slicer", "value")
)
def return_select_server(value):
    global server
    global original_df
    values = days_list
    v_in = values[value[0]:value[1]+1]
    df = pandas.DataFrame()
    df = global_df
    df2 = pandas.DataFrame()
    a = 0
    for i in v_in:
        if a == 0:
            df2 = df.loc[df["DATE"] == i]
            a += 1
        else:
            df2 = pandas.concat([df2, df.loc[df["DATE"] == i]])
    original_df = df2
    return [dcc.RadioItems(id = "select_server", options = ["all", "quranic", "ebad", "motaghin"], value = server)]
# 2:    Create a field to specify the server and update the database and specify figures 
# >>>   This requires several steps that have been identified
#         #
#      #  #  # 
#       # # #
#         #
#
# 2-1:  Output for map
@app.callback(
    Output("output_map", "figure"),
    Input("select_server", "value")
)
def select_server_for_map(value):
    global server
    server = value # To keep the server address after the change
    global original_df
    df = original_df
    map_df = pandas.DataFrame()
    if value == "motaghin":
        map_df = df.loc[df["SERVER"] == "motaghin.quranic.network"]
    elif value == "quranic":
        map_df = df.loc[df["SERVER"] == "quranic.network"]
    elif value == "ebad":
        map_df = df.loc[df["SERVER"] == "ebad.quranic.network"]
    elif value == "all":
        map_df = df
    map_fig = px.scatter_mapbox(
        data_frame = map_df,
        lat = "LAT",
        lon = "LON",
        mapbox_style = "open-street-map",
        color_discrete_sequence = ["#48D1CC"],
        hover_name = "NAME",
        hover_data = ["CITY"],
        zoom = 3,
        title = "locations",
        animation_frame = "DATE TIME",
        height = 800,
    )
    return map_fig
# 2-2:  Output for histogram
@app.callback(
    Output("output_histogram", "figure"),
    Input("select_server", "value")
)
def select_server_for_histogram(value):
    df = original_df
    histogram_df = pandas.DataFrame()
    if value == "motaghin":
        histogram_df = df.loc[df["SERVER"] == "motaghin.quranic.network"]
    elif value == "quranic":
        histogram_df = df.loc[df["SERVER"] == "quranic.network"]
    elif value == "ebad":
        histogram_df = df.loc[df["SERVER"] == "ebad.quranic.network"]
    elif value == "all":
        histogram_df = df
    his_fig = px.histogram(
        data_frame = histogram_df,
        x = "DATE TIME",
        y = "LOGIN NUMBER",
        title = "login time",
    )
    his_fig.update_xaxes(
        rangeslider_visible = True,
        rangeselector = dict(
            buttons = list([
                dict(label = "1d", step = "day"),
                dict(label = "all", step = "all")
            ])
        ),
    )
    return his_fig
#
#
#   #    #  ######  #        #  #########
#   ##   #  #         #   #         #    
#   # #  #  ######      #           #    
#   #  # #  #         #   #         #    
#   #    #  ######  #        #      #    
#
#
#  #       ######  #       #  ######  #     
#  #       #        #     #   #       #     
#  #       ######    #   #    ######  #     
#  #       #          # #     #       #     
#  ######  ######      #      ######  ######
#
# Build app layout and runserver
app.layout = html.Div([
    html.Div(id = "return_select_server"),
    dcc.Graph(id = "output_map"),
    html.P(id = "output_slicer"),
    dcc.RangeSlider(0, len(days_list)-1, 1, None, [len(days_list)-2, len(days_list)-1], id = "input_slicer"),
    dcc.Graph(id = "output_histogram")
    ])
app.run_server(debug = False, host = os.getenv("HOST", "127.0.0.1"), port = os.getenv("PORT", "8453"))
