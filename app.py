from dash_bootstrap_components._components.Label import Label
from fetch_data import fetch_profile, fetch_fundementals, fetch_stock_list
import dash
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from geopandas.tools import geocode
import pandas_datareader.data as web
from datetime import date, datetime
# elements

all_stocks = fetch_stock_list()

description_card = dbc.Card(
    [
        dbc.CardHeader("Company Description"),
        dbc.CardBody(
            [
                dbc.Spinner(
                    html.P(id='description', className='card-text')
                )
            ]
        )
    ],
)

fundementals_cards = dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Return on Equity', className='card-title'),
                    html.P(id='ROE', className='card-text')
                ]
            )
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Market Cap', className='card-title'),
                    html.P(id='market_cap', className='card-text')
                ]
            ),
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Profit Margin', className='card-title'),
                    html.P(id='profit_margin', className='card-text')
                ]
            ),
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('Revenue TTM', className='card-title'),
                    html.P(id='revenue_ttm', className='card-text')
                ]
            ),
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('EPS', className='card-title'),
                    html.P(id='eps', className='card-text')
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5('PE Ratio', className='card-title'),
                    html.P(id='pe', className='card-text')
                ]
            ),
        ),
    ]
)

forcast_card = dbc.CardDeck(
    [

    ]
)

# the application

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

server = app.server

marks = {i: str(i) for i in range(0, 91, 10)}

app.layout = html.Div(
    [
        html.Br(),
        html.H2("Stock Analysis", style={'display': 'inline'}),
        html.Img(id='logo', style={'display': 'inline', 'height': '3%',
                 'width': '3%', 'margin-left': '2%', 'margin-bottom': '1%'}),
        html.Br(),
        dcc.Dropdown(
            id='stock',
            options=[{'label': row['name'] + ' | ' + row['symbol'],
                      'value': row['symbol']} for index, row in all_stocks.iterrows()],
            value='AAPL'
        ),
        html.Br(),
        dbc.Alert(
            "This project is still under development",
            dismissable=True,
            color='secondary'
        ),
        dbc.Alert(
            "Failed to retrieve company profile",
            id="profile_failure",
            dismissable=True,
            is_open=False,
            color='warning',
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        description_card
                    ]
                ),
                dbc.Col(
                    [
                        dbc.CardDeck(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Industry"),
                                        dbc.CardBody(
                                            html.P(id="industry"),
                                        )
                                    ]
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader("CEO"),
                                        dbc.CardBody(
                                            [
                                                html.P(id="ceo")
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Card(
                            [
                                dbc.CardHeader('Company Location'),
                                dbc.CardBody(
                                    dbc.Spinner(
                                        dcc.Graph(id='address')
                                    ),
                                )
                            ]
                        )
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Alert(
            "Failed to retrieve fundementals",
            id='fund_failure',
            is_open=False,
            dismissable=True,
            color='warning',
        ),
        fundementals_cards,
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader('Stock Historical Data'),
                dbc.CardBody(
                    [
                        dbc.Alert(
                            "Failed to retrieve stock data",
                            id='stock_failure',
                            is_open=False,
                            dismissable=True,
                            color='warning',
                        ),
                        dcc.DatePickerRange(
                            id='stock_range',
                            min_date_allowed=date(1985, 1, 1),
                            max_date_allowed=datetime.now(),
                            start_date=date(2018, 1, 1),
                            end_date=datetime.now()
                        ),
                        html.Br(),
                        dbc.Spinner(
                            dcc.Graph(id='stock_historical'),
                        ),
                        dbc.Row(
                            [
                                dbc.Col(

                                    dbc.Card(
                                        dcc.Graph(id='dist_plot'),
                                    ),
                                    width=6,
                                ),
                                dbc.Col(

                                    dbc.Card(
                                        dcc.Graph(id='log_plot'),
                                    ),
                                    width=6,
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader('Stock Forcast ML'),
                dbc.CardBody(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Pick the dates to feed the model'),
                                html.Br(),
                                dcc.DatePickerRange(
                                    id='fit_range',
                                    min_date_allowed=date(2000, 1, 1),
                                    max_date_allowed=datetime.now(),
                                    start_date=date(2005, 1, 1),
                                    end_date=datetime.now(),
                                    # style={'display:inline-block'}
                                ),
                                html.Br(),
                                dbc.Label('Pick how far into the future (in days) do you want the model to predict'),
                                dcc.Slider(
                                    id='period',
                                    min=10,
                                    max=90,
                                    step=10,
                                    value=10,
                                    marks=marks
                                ),
                                html.Br(),
                                dbc.Spinner(
                                    dcc.Graph(id='forecast'),
                                ),
                            ],
                            width=6
                        ),
                    ]
                )
            ]
        )

    ],
    style={'margin-right': '3%', 'margin-left': '3%'}
)


@app.callback(
    [
        Output('description', 'children'),
        Output('address', 'figure'),
        Output('profile_failure', 'is_open'),
        Output('ceo', 'children'),
        Output('industry', 'children'),
        Output('logo', 'src')
    ],
    Input('stock', 'value')
)
def update_description(symbol):
    alert = False
    profile = fetch_profile(symbol)

    try:
        img = profile['image'][0]
        desc = profile['description'][0]
        ceo = profile['ceo'][0]
        industry = profile['industry'][0]
        location = "{}, {}, {}, {}".format(
            profile['address'][0], profile['city'][0], profile['state'][0], profile['country'][0])
        locations = geocode(location, provider='nominatim',
                            user_agent='my_app')

        fig = px.scatter_mapbox(
            lat=locations['geometry'].y,
            lon=locations['geometry'].x,
            mapbox_style='carto-positron',
            zoom=15,
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
        )

        fig.update_traces(marker=dict(size=12, color='red'))
    except:
        alert = True
        desc = "N/A"
        fig = px.scatter()
        img = ""
        ceo = 'N/A'
        industry = 'N/A'

    return desc, fig, alert, ceo, industry, img


@app.callback(
    [
        Output('market_cap', 'children'),
        Output('ROE', 'children'),
        Output('profit_margin', 'children'),
        Output('revenue_ttm', 'children'),
        Output('eps', 'children'),
        Output('pe', 'children'),
        Output('fund_failure', 'is_open')
    ],
    Input('stock', 'value'),
)
def update_fundementals(symbol):
    alert = False
    try:
        df = fetch_fundementals(symbol)
        market_cap = "{:,}".format(int(df['MarketCapitalization'][0]))
        ROE = df['ReturnOnEquityTTM'][0]
        profit_marg = "{:.0%}".format(float(df['ProfitMargin'][0]))
        revenue = "{:,}".format(int(df['RevenueTTM'][0]))
        EPS = df['EPS'][0]
        PE = df['PERatio'][0]
    except:
        market_cap = "N/A"
        ROE = "N/A"
        profit_marg = "N/A"
        revenue = "N/A"
        EPS = "N/A"
        PE = "N/A"
        alert = True

    return market_cap, ROE, profit_marg, revenue, EPS, PE, alert


@app.callback(
    [
        Output('stock_historical', 'figure'),
        Output('stock_failure', 'is_open'),
        Output('dist_plot', 'figure'),
        Output('log_plot', 'figure')
    ],
    [
        Input('stock', 'value'),
        Input('stock_range', 'start_date'),
        Input('stock_range', 'end_date')
    ]
)
def update_stock(symbol, start, end):
    alert = False
    try:
        df = web.DataReader(symbol, 'yahoo', start, end)
        fig = px.line(x=df.index, y=df['Open'], labels={
                      'y': 'Price in $', 'x': ''})
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
            template='plotly_white'
        )
        returns = (df['Close'] - df['Open']) / df['Open']
        avg = returns.mean()
        dist = px.histogram(returns, histnorm='probability density', labels={
                            'value': 'returns'})
        dist.add_vline(x=0, line_width=2, line_dash='dash', line_color='red')
        # dist.add_vline(x=avg, line_width=2, line_dash='dash', line_color='green', name='average')
        log_plot = px.line(x=df.index, y=df['Close'], labels={
                           'y': 'Log Scale Price in $', 'x': ''}, log_y=True)
        dist.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
            template='plotly_white'
        )
        log_plot.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
            template='plotly_white'
        )
    except:
        alert = True
        fig = px.line()
        log_plot = px.line()
        dist = px.histogram()
    return fig, alert, dist, log_plot


@app.callback(
    Output('forecast', 'figure'),
    [
        Input('period', 'value'),
        Input('fit_range', 'start_date'),
        Input('fit_range', 'end_date'),
        Input('stock', 'value')
    ]
)
def update_stock_forecast(period, start, end, symbol):
    from ml_model import stock_predict
    plt = stock_predict(symbol, start, end, period)
    plt.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        template='plotly_white'
    )
    return plt


if __name__ == '__main__':
    app.run_server(debug=True)
