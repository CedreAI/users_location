# libraries
import pandas
import plotly.express as px
from dash import Dash, html, Input, Output, dcc
from persiantools.jdatetime import JalaliDate
from random import randint

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
# set figurs
#         #
#      #  #  # 
#       # # #
#         #
#
# 1:    set map figures
map_fig = px.scatter_mapbox(
    data_frame = original_df,
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
#         @
# 2:    set histogram figur
his_fig = px.histogram(
    data_frame = original_df,
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
# 1-1:    Output for map
@app.callback(
    Output("output_map", "children"),
    Input("input_slicer", "value")
)
def map_update_layout(value):
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
    map_fig.update_layout(data_frame = original_df,) # This line gives an error; Due to "data_frame = original_df"
    return [dcc.Graph(figure = map_fig)]



app.layout = html.Div([
    html.Div(id = "output_map"),
    # html.Div([dcc.RangeSlider(0, len(list_days)-1, 1, marks = None, value = [len(list_days)-2, len(list_days)-1], id = "input_slicer")]),
    dcc.RangeSlider(0, len(days_list)-1, 1, None, [len(days_list)-2, len(days_list)-1], id = "input_slicer")
    ])

app.run_server(debug = True)
