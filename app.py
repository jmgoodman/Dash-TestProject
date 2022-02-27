import dash
import dash_core_components as dcc # from dash import dcc
import dash_html_components as html # from dash import html
import pandas as pd

data = pd.read_csv("avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True) # inplace = transform original data, don't make a copy

app = dash.Dash(__name__) # On line 11, you create an instance of the Dash class. 
                          # If you’ve used Flask before, then initializing a Dash class may look familiar. 
                          # In Flask, you usually initialize a WSGI application using Flask(__name__). 
                          # Similarly, for a Dash app, you use Dash(__name__).
                          # (i.e., this is boilerplate which initializes the class housing your dang app!)


# define the app html markup
# the html tools are funny, since it doesn't really save you time, just slightly changes the syntax from tags to functions that wrap your elements in tags
app.layout = html.Div(
    children=[
        html.H1(children="Avocado Analytics",),
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

if __name__ == "__main__": # guards against accidental automatic calling by a higher-level process (i.e., an import) ("if __main__" means that app.py is the top-level call)
    app.run_server(debug=True) # debug=True enables dev tools