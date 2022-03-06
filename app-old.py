# %%
import dash
import dash_core_components as dcc # from dash import dcc
import dash_html_components as html # from dash import html
import pandas as pd
from datetime import timedelta
import numpy as np

# foreward: find your preferred emoji favicon here: https://favicon.io/emoji-favicons/
# download it and stuff at LEAST the .ico file into your assets folder, which then gets served automatically

data = pd.read_csv("avocado.csv") # https://www.kaggle.com/neuromusic/avocado-prices
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True) # inplace = transform original data, don't make a copy

# get rolling averages
data["RollingAveragePrice"] = data["AveragePrice"].rolling(4,min_periods=1).mean()
data["RollingAverageVolume"] = data["Total Volume"].rolling(4,min_periods=1).mean()


# these data could stand to be smoothed for visual appeal...
# ...and a cursory glance suggests uniform sampling
# so, I could probably just use out-of-the-box smoothing routines
# ...except pandas rolling with datetime argument handles nonuniform sampling out-of-the-box too, I think?
# ehhh it's a little more complicated than that. see: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html
# just assume uniform weekly sampling and your 4-long window for it, mkay?
# the behavior of pandas.rolling is quite BAFFLING. Sometimes it works, sometimes it doesn't, it all depends on which combinations of non-numeric columns I decide to leave in or not
# the problem seems to be that it was simply never meant to be used with more than one column at once.
# %%
# add external stylesheet info, add it as an optional second input to dash.Dash
"""
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
] # so... is this a list of 1 dict? it seems like this framework loves to think of things as lists of dicts (I imagine dicts are how html tags are stored, and naturally you might want to specify a list of html elements for some parts, hence list-of-dicts conventions for at least some parts of the framework, which I imagine percolates elsewhere for, at the very least, consistency's sake. feels clunky though.)
"""
# print("Hello""World") # test, just appends the two strings
external_stylesheets = [
    dict([
        ('href','https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'),
        ('rel','stylesheet')
    ])
] # note: the split into two strings earlier didn't do anything, it was just a way to try and make it neater by taking advantage of automatic concatenation of adjacent strings, then splitting them up onto different lines.
# so this is, indeed, equivalent. idk what this does yet, it doesn't seem to do anything. Maybe it's referenced in the css file I donwloaded?

# print(__name__) # debug / testing, prints __main__ when app.py is a top-level call and not imported from a script higher up in the chain. I am dumb and do not yet see the utility of this, but it seems awfully fundamental. Its typical use cases seem related to checking to see a code's run context to determine certain behaviors that would make sense in a top-level but not an imported call.

# surrogate pair is a javascript thing and python shouldn't allow it without clunky handlers. Just use a 32-bit specification: https://stackoverflow.com/questions/38147259/how-can-i-convert-surrogate-pairs-to-normal-string-in-python
# print("\U0001f35e") # debug: bread emoji using python syntax for unicode parsing

app = dash.Dash(__name__, external_stylesheets=external_stylesheets) # On line 11, you create an instance of the Dash class. 
                          # If you’ve used Flask before, then initializing a Dash class may look familiar. 
                          # In Flask, you usually initialize a WSGI application using Flask(__name__). 
                          # Similarly, for a Dash app, you use Dash(__name__).
                          # (i.e., this is boilerplate which initializes the class housing your dang app!)
app.title = "Avocado Analytics: Grab Some \U0001f35e Toast \U0001f35e"
# define the app html markup (which needs to happen inside app.layout!!!)
# the html tools are funny, since it doesn't really save you time, just puts it all in your python context. which I guess helps psychologically anyway.

# less-scalable text styling
# style = dict([
#   (propname,propval),
#   (propname,propval)
# ])

# down below:
# "displaymodebar" toggles whether the plot visualization toolbar (pan, zoom, etc.) shows up (ideally you curate the style yourself and hide this clutter from the user)
# manually giving <extra> tags to the hovertemplate lets you control the info that pops up NEXT to the value - default is to display the variable name from the legend (specified in the "name" entry). Having this empty reduces clutter.
# I never explicitly define "header" class in my css file, so I assume this is given in the external stylesheet I imported above...
# no "%" symbols in tick formats unless you want % literals
# classname card makes a box for the plot to be in
# classname wrapper imposes a max width fixed margins on its contents
# okay, I found the docs for numeric formatting based on the d3 standard: https://github.com/d3/d3-3.x-api-reference/blob/master/Formatting.md#d3_forma
# and for datetime: https://github.com/d3/d3-time-format
app.layout = html.Div(
    children=[        
        html.Div(
            children=[
                html.P(children="\U0001f951", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="price-chart",
                            config={"displayModeBar": False},
                            figure={
                                "data": [
                                    {
                                        "x": data["Date"],
                                        "y": data["AveragePrice"],
                                        "type": "lines",
                                        "name": "Weekly Price",
                                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                                    },
                                    {
                                        "x": data["Date"],
                                        "y": data["RollingAveragePrice"],
                                        "type": "lines",
                                        "name": "4-Week Rolling Average Price",
                                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                                    },
                                ],
                                "layout": {
                                    "title": {
                                        "text": "Average Price of Avocados",
                                        "x": 0.05,
                                        "xanchor": "left",
                                    },
                                    "xaxis": {"fixedrange": True},
                                    "yaxis": {
                                        "tickprefix": "$",
                                        "fixedrange": True,
                                        "tickformat": "0.2f"
                                    },
                                    "colorway": ["#CACFCE",
                                        "#17B897"],
                                },
                            },
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="volume-chart",
                            config={'displayModeBar': False},
                            figure={
                                "data": [
                                    {
                                        "x": data["Date"],
                                        "y": data["Total Volume"],
                                        "customdata": data["Total Volume"] // 1000,
                                        "type": "lines",
                                        "name": "Weekly Volume",
                                        "hovertemplate": "%{customdata:d}k<extra></extra>",
                                    },
                                    {
                                        "x": data["Date"],
                                        "y": data["RollingAverageVolume"],
                                        "customdata": data["RollingAverageVolume"] // 1000,
                                        "type": "lines",
                                        "name": "4-Week Rolling Average Volume",
                                        "hovertemplate": "%{customdata:d}k<extra></extra>",
                                    },
                                ],
                                "layout": {
                                    "title": {
                                        "text": "Avocados Sold",
                                        "x": 0.05,
                                        "xanchor": "left",
                                    },
                                    "xaxis": {"fixedrange": True},
                                    "yaxis": {"fixedrange": True},
                                    "colorway": ["#CACFCE",
                                                 "#E12D39"],
                                },
                            }, 
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ],
)

# Under the hood, Dash uses Plotly.js to generate graphs. 
# The dcc.Graph components expect a figure object or a (list of!) 
# # Python dictionar(ies!) containing the plot’s data and layout. 
# # In this case, you provide the latter.

# practice corroborated by the official dash documentation: https://dash.plotly.com/deployment
if __name__ == "__main__": # if this is called as the top-level call (i.e., in a typical debug setting), start a production server (werkzeug) - https://community.plotly.com/t/production-and-development-enviroments/21348
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(debug=True,port=8888) # debug=True enables dev tools, here is the official documenation: https://dash.plotly.com/reference#app.run_server