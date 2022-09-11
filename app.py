import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from fin_functions import *


# Initial values for chart
c_p ='c'
S = 21000
K = 21000 # value 0 will cause divide by 0 error in S/K
r = 0.01
T = 0.1
q = 0
sigma = 0.7
min_range = 0
max_range = 2*K


# Build Dash App #################################################################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Layout Elements
controls = html.Div(
    [
    
    html.H2('Parameters'),
    html.Hr(),
    
    # add input for step size again so user can decide for which Price Underlyings he sees option prices 
    html.Br(),
    html.Table(children=[
        html.P('Option Type', style={'font_size': '16px', 'verticalAlign': 'top', 'display':'inline-block','width':'125px'}),
    dcc.Dropdown(id='call_put', options=[
        {'label': 'Call', 'value': 'c'},
        {'label': 'Put', 'value': 'p'}], value=c_p, style={'display':'inline-block','width':'225px'}),
                        ]
              ),
    
    html.Br(),
    html.Table(children=[
        html.P('Strike Price', style={'font_size': '16px', 'verticalAlign': 'top', 'display':'inline-block','width':'125px'}),
        dcc.Input(id='k-input', value=K, type="number", min=0, style={'display':'inline-block','width':'225px'}),
                         ]
              ),

    html.Br(),
    html.Table(children=[
        html.P('Interest Rate', style={'font_size': '16px', 'verticalAlign': 'top', 'display':'inline-block','width':'125px'}),
        dcc.Input(id='r-input', value=r, type="number", min=0, style={'display':'inline-block','width':'225px'}),
                         ]
              ),

    html.Br(),
    html.Table(children=[
        html.P('Time to Maturity', style={'font_size': '16px', 'verticalAlign': 'top', 'display':'inline-block','width':'125px'}),
    dcc.Input(id='t-input', value=T, type="number", min=0, style={'display':'inline-block','width':'225px'}),
                         ]
              ),

    html.Br(),
    html.Table(children=[
        html.P('Dividend Yield', style={'font_size': '16px', 'verticalAlign': 'top', 'display':'inline-block','width':'125px'}),
        dcc.Input(id='q-input', value=q, type="number", min=0, style={'display':'inline-block','width':'225px'}),
                         ]
              ),

    html.Br(),
    html.Table(children=[
        html.P('Volatility', style={'font_size': '16px', 'verticalAlign': 'top', 'display':'inline-block','width':'125px'}),
        dcc.Input(id='sigma-input', value=sigma, type="number", min=0, style={'display':'inline-block','width':'225px'}),
                         ]
              ),   

    ]
)

# Plot
graphic = html.Div(
    [
        html.H2('Output'),
        html.Hr(),
        dcc.Graph(id='option price', 
                  figure=px.line(create_data(min_range, max_range, c_p, K, r, T, q, sigma), 
                  x="Price Underlying", y="Option Price",  markers=True),
                 ),
    ]
)

# Layout
app.layout = html.Div(children=[
    
    html.Div(controls, style={'width': '29%', 'min-width': '360px', 'vertical-align': 'top', 'marginLeft': '1%', 'display': 'inline-block', 'justify-content': 'space-between', 'flex-wrap': 'wrap', 'float': 'left'}),
    html.Div(graphic, style={'width': '68%', 'min-width': '400px', 'vertical-align': 'top', 'marginLeft': '1%', 'marginRight': '1%', 'display': 'inline-block', 'justify-content': 'space-between', 'flex-wrap': 'wrap', 'float': 'left'}),
])


# Define callback to update graph
@app.callback(
     Output('option price', 'figure'),
     Input('call_put', 'value'),
     Input('k-input', 'value'),
     Input('r-input', 'value'),
     Input('t-input', 'value'),
     Input('q-input', 'value'),
     Input('sigma-input', 'value')
)

# Update graph on change of inputs
def update_figure(call_put, k_input, r_input, t_input, q_input, sigma_input):
    fig = px.line(create_data(min_range, max_range, call_put, k_input, r_input, t_input, q_input, sigma_input), x="Price Underlying", y="Option Price", markers=True)
    fig.update_layout(transition_duration=500)
    return fig
    
# Run app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8080)
