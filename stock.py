from flask import Flask
import pandas_datareader.data as web
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.config.suppress_callback_exceptions = True

app.title = 'AMStock'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

])

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

def pct_change(open_price,current_price):
    pct = ((current_price-open_price)/open_price)*100
    return round(pct,3)

def pct_change_formatter(pct_change):
    PCT_COLOR = "center-align text-danger"
    if pct_change>0:
        pct_string = "+"+str(round(pct_change,2))+"%"
        PCT_COLOR = "center-align text-success"
    else:
        pct_string = str(round(pct_change,2))+"%"
    return (pct_string, PCT_COLOR)

symbols=pd.read_csv('Symbols.csv')
def get_name(msg):
    for i in range(len(symbols['Symbol'])):
        if msg==symbols['Symbol'][i]:
            return symbols['Company'][i]+' '+'('+msg+')'
    else:
        return msg

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname==None:
        return html.Div([
            html.H3('ERROR 404')
        ])
    else:
        s = pathname.split('/')
        stock = s[1]
        start_date = dt.datetime(2015, 1, 1)
        end_date = dt.datetime.now()
        df = web.DataReader(stock, 'yahoo', start_date, end_date)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)


        pct_changes, COLOR = pct_change_formatter(pct_change(df['Close'][-2], df['Close'][-1]))
        layout1 = go.Layout({
            "legend": {"orientation": "h", "xanchor": "right"},
            "xaxis": {
                "rangeselector": {
                    "buttons": [
                        {"count": 1, "label": "1D", "step": "day",
                         "stepmode": "backward"},
                        {"count": 5, "label": "5D", "step": "day",
                         "stepmode": "backward"},
                        {"count": 6, "label": "6M", "step": "month",
                         "stepmode": "backward"},
                        {"count": 1, "label": "1Y", "step": "year",
                         "stepmode": "backward"},
                        {"count": 1, "label": "YTD", "step": "year",
                         "stepmode": "todate"},
                        {"label": "5Y", "step": "all",
                         "stepmode": "backward"}
                    ]
                }}})

        return (
            html.H1(className="center-align big-title", children=[get_name(stock)]),
            html.Div(className="row", children=[

            html.Div([dcc.Graph(id='graph',
            figure={'data': [{'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock},],
                    'layout': layout1},
            config={'displayModeBar': False})]),

            html.Div(className="col-lg-4", children=[
            html.Div(className='container top-margin', children=[
            html.Div(className="col-sm-6", children=[
            html.H1(className="center-align big-title", children=["Details"]), ]),

            html.Div(className="row", children=[html.Div(className="col-sm-6", children=[
            html.H6(className="center-align", children=["Close"]),
            html.H4(className="center-align", children=[round(df['Close'][-1], 2)])]),

            html.Div(className="col-sm-6", children=[
            html.H6(className="center-align", children=["Percent"]),
            html.H5(className=COLOR, children=[pct_changes])])]),

            html.Div(className="row", children=[html.Div(className="col-sm-6", children=[
            html.H6(className="center-align", children=["Open"]),
            html.H4(className="center-align", children=[round(df['Open'][-1],2)])]),

            html.Div(className="col-sm-6", children=[
            html.H6(className="center-align", children=["High"]),
            html.H4(className="center-align", children=[round(df['High'][-1],2)])])]),

            html.Div(className="row", children=[html.Div(className="col-sm-6", children=[
            html.H6(className="center-align", children=["Low"]),
            html.H4(className="center-align", children=[round(df['Low'][-1],4)])]),

            html.Div(className="col-sm-6", children=[html.H6(className="center-align", children=["Volume"]),
            html.H4(className="center-align", children=[df['Volume'][-1]])])])])])]))


if __name__ == "__main__":
    app.run_server(debug=True)