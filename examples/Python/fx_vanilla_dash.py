
"""Mini Dash app for FX vanilla option pricing in qflib."""

import numpy as np
import dash
from dash import Input, Output, dcc, html

from qflib.qflib import fx_vanilla_price

DEFAULTS = {
    'spot': 1.05,
    'strike': 1.05,
    'time_to_expiry': 0.5,
    'domestic_rate': 0.02,
    'foreign_rate': 0.01,
    'volatility': 0.15,
    'option_type': 'call',
}

app = dash.Dash(__name__)
app.title = 'FX Vanilla Pricing'


def _build_price_table(result):
    rows = [
        ('Price', result['price']),
        ('Delta', result['delta']),
        ('Gamma', result['gamma']),
        ('Vega', result['vega']),
    ]
    return html.Table([
        html.Thead(html.Tr([html.Th('Metric'), html.Th('Value')])),
        html.Tbody([
            html.Tr([html.Td(label), html.Td(f"{value:0.6f}")]) for label, value in rows
        ]),
    ], className='price-table')


def _build_surface_figure(spot, time_to_expiry, domestic_rate, foreign_rate, volatility):
    strike_grid = np.linspace(0.6 * spot, 1.4 * spot, 41)
    call_curve = []
    put_curve = []
    for grid_strike in strike_grid:
        params = (spot, float(grid_strike), time_to_expiry, domestic_rate, foreign_rate, volatility)
        call_curve.append(fx_vanilla_price(*params, option_type='call')['price'])
        put_curve.append(fx_vanilla_price(*params, option_type='put')['price'])

    figure = {
        'data': [
            {'x': strike_grid.tolist(), 'y': call_curve, 'mode': 'lines', 'name': 'Call'},
            {'x': strike_grid.tolist(), 'y': put_curve, 'mode': 'lines', 'name': 'Put'},
        ],
        'layout': {
            'title': 'Price vs Strike (surface slice)',
            'xaxis': {'title': 'Strike'},
            'yaxis': {'title': 'Option Price'},
            'legend': {'orientation': 'h'},
            'margin': {'l': 60, 'r': 10, 't': 40, 'b': 50},
        },
    }
    return figure


app.layout = html.Div([
    html.H2('FX Vanilla Option (Garman-Kohlhagen)'),
    html.Div([
        html.Label('Spot'),
        dcc.Input(id='spot-input', type='number', value=DEFAULTS['spot'], step=0.01),
        html.Label('Strike'),
        dcc.Input(id='strike-input', type='number', value=DEFAULTS['strike'], step=0.01),
        html.Label('Time to Expiry (yrs)'),
        dcc.Input(id='time-input', type='number', value=DEFAULTS['time_to_expiry'], step=0.05, min=0),
        html.Label('Domestic Rate'),
        dcc.Input(id='dom-rate-input', type='number', value=DEFAULTS['domestic_rate'], step=0.005),
        html.Label('Foreign Rate'),
        dcc.Input(id='for-rate-input', type='number', value=DEFAULTS['foreign_rate'], step=0.005),
        html.Label('Volatility'),
        dcc.Input(id='vol-input', type='number', value=DEFAULTS['volatility'], step=0.01, min=0),
        html.Label('Option Type'),
        dcc.Dropdown(
            id='option-type-dropdown',
            options=[{'label': 'Call', 'value': 'call'}, {'label': 'Put', 'value': 'put'}],
            value=DEFAULTS['option_type'],
            clearable=False,
        ),
    ], className='controls'),
    html.Div(id='price-output'),
    dcc.Graph(id='surface-graph'),
], className='container')


@app.callback(
    Output('price-output', 'children'),
    Output('surface-graph', 'figure'),
    Input('spot-input', 'value'),
    Input('strike-input', 'value'),
    Input('time-input', 'value'),
    Input('dom-rate-input', 'value'),
    Input('for-rate-input', 'value'),
    Input('vol-input', 'value'),
    Input('option-type-dropdown', 'value'),
)
def update_outputs(spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility, option_type):
    if None in (spot, strike, time_to_expiry, domestic_rate, foreign_rate, volatility) or option_type is None:
        return dash.no_update, dash.no_update

    result = fx_vanilla_price(float(spot), float(strike), float(time_to_expiry),
                              float(domestic_rate), float(foreign_rate), float(volatility), option_type)
    table = _build_price_table(result)
    figure = _build_surface_figure(float(spot), float(time_to_expiry), float(domestic_rate),
                                   float(foreign_rate), float(volatility))
    return table, figure


if __name__ == '__main__':
    app.run_server(debug=True)
