import pandas
import plotly.express as px
from persiantools.jdatetime import JalaliDate as jd

# data bise
df_original = pandas.read_csv("database/visitors.tsv", sep = "\t")
date = []
for i in df_original["DATE"]:
    date.append(jd.to_jalali(int(i.split("-")[0]), int(i.split("-")[1]), int(i.split("-")[2])))

df_original["DATE"] = date



# dash
from dash import Dash, html, Input, Output, dcc


app = Dash(title = "map")

# slicer
dic = {}
for i in df_original["DATE"]:
    dic[i] = 0
list_days = list(dic.keys())

dic_day = {}
n = -1
for i in list_days:
    n += 1
    dic_day[n] = i

@app.callback(
    Output("map_output", "children"),
    [Input("slicer_input", "value")]
)
def map(value):
    values = list(dic_day.values())
    v_in = values[value[0]:value[1]+1]
    df = pandas.read_csv("visitor.tsv", "\t")

    date = []
    for i in df["DATE"]:
        date.append(jd.to_jalali(int(i.split("-")[0]), int(i.split("-")[1]), int(i.split("-")[2])))

    df["DATE"] = date


    dh = []
    for i in df["DATE TIME LOGIN"]:
        dh.append(jd.to_jalali(int(i.split(" ")[0].split("-")[0]), int(i.split(" ")[0].split("-")[1]), int(i.split(" ")[0].split("-")[2])).isoformat() + " " + i.split(" ")[1].split(":")[0] + ":00")
    df["date time"] = dh
    

    df2 = pandas.DataFrame()
    a = 0
    for i in v_in:
        if a == 0:
            df2 = df.loc[df["DATE"] == i]
            a += 1
        else:
            df2 = pandas.concat([df2, df.loc[df["DATE"] == i]])
    df_original = df2
    

    # map
    fig_map = px.scatter_mapbox(
        data_frame = df_original,
        lat = "LAT",
        lon = "LON",
        mapbox_style = "open-street-map",
        color_discrete_sequence = ["#48D1CC"],
        hover_name = "NAME",
        hover_data = ["CITY"],
        zoom = 3,
        title = "location",
        animation_frame = "date time",
        height = 800,
    )

    
    return [dcc.Graph(figure = fig_map)]


@app.callback(
    Output("output", "children"),
    [Input("slicer_input", "value")]
)
def output(value):
    values = list(dic_day.values())
    v_in = values[value[0]:value[1]+1]
    return f"[{v_in[0]}, {v_in[-1]}]"

@app.callback(
    Output("histogram_output", "children"),
    [Input("slicer_input", "value")]
)
def histogram(value):
    values = list(dic_day.values())
    v_in = values[value[0]:value[1]+1]
    df = pandas.read_csv("visitor.tsv", "\t")

    date = []
    for i in df["DATE"]:
        date.append(jd.to_jalali(int(i.split("-")[0]), int(i.split("-")[1]), int(i.split("-")[2])))

    df["DATE"] = date


    dh = []
    for i in df["DATE TIME LOGIN"]:
        dh.append(jd.to_jalali(int(i.split(" ")[0].split("-")[0]), int(i.split(" ")[0].split("-")[1]), int(i.split(" ")[0].split("-")[2])).isoformat() + " " + i.split(" ")[1].split(":")[0] + ":00")
    df["date time"] = dh
    

    df2 = pandas.DataFrame()
    a = 0
    for i in v_in:
        if a == 0:
            df2 = df.loc[df["DATE"] == i]
            a += 1
        else:
            df2 = pandas.concat([df2, df.loc[df["DATE"] == i]])
    df_original = df2

    # histogram

    val_log = []
    for i in df_original["date time"]:
        val_log.append(1)#values[n])


    df_original["login"] = val_log

    fig_his = px.histogram(
        data_frame = df_original,
        x = "date time",
        y = "login",
        title = "login time",
    )
    fig_his.update_xaxes(
        rangeslider_visible = True,
        rangeselector = dict(
            buttons = list([
                dict(label = "1d", step = "day"),
                dict(label = "all", step = "all")
            ])
        ),
    )
    return [dcc.Graph(figure = fig_his)]






# layout

app.layout = html.Div([
    html.Div(id = "map_output"),
    html.P(id = "output", style = {"family-font":"SENS"}),
    html.Div([dcc.RangeSlider(0, len(list(dic_day.values()))-1, 1, marks = None, value = [len(list(dic.values()))-2, len(list(dic.values()))-1], id = "slicer_input"),]),
    html.Div(id = "histogram_output")
])

import os
app.run_server(host = os.getenv("HOST", "127.0.0.1"), port = os.getenv("PORT", "8453"), debug = True)
