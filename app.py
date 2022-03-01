import dash
import dash_core_components as dcc # from dash import dcc
import dash_html_components as html # from dash import html
import pandas as pd

# foreward: find your preferred emoji favicon here: https://favicon.io/emoji-favicons/
# download it and stuff at LEAST the .ico file into your assets folder, which then gets served automatically

data = pd.read_csv("avocado.csv") # https://www.kaggle.com/neuromusic/avocado-prices
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True) # inplace = transform original data, don't make a copy

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
# so this is, indeed, equivalent. idk what this does yet, it doesn't seem to do anything.

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

app.layout = html.Div(
    children=[        
        html.H1(children="Avocado Analytics",
                className="header-title",
        ),
        
        html.P(
            children="Analyze the behavior of avocado prices"
            " and the number of avocados sold in the US"
            " between 2015 and 2018",
        ),
        
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados Sold"},
            }, # Under the hood, Dash uses Plotly.js to generate graphs. 
            # The dcc.Graph components expect a figure object or a (list of!) 
            # # Python dictionar(ies!) containing the plot’s data and layout. 
            # # In this case, you provide the latter.
        ),
    ]
)

# practice corroborated by the official dash documentation: https://dash.plotly.com/deployment
if __name__ == "__main__": # if this is called as the top-level call (i.e., in a typical debug setting), start a production server (werkzeug) - https://community.plotly.com/t/production-and-development-enviroments/21348
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(debug=True) # debug=True enables dev tools, here is the official documenation: https://dash.plotly.com/reference#app.run_server
    