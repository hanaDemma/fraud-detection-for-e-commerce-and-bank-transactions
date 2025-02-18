# app.py
from flask import Flask, jsonify
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Initialize Flask app
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Load and preprocess data
def load_data(filename):
    df = pd.read_csv(filename)
    df['purchase_time'] = pd.to_datetime(df['purchase_time'])
    df['class'] = df['class'].astype(int)
    return df

fraud_df = load_data('Fraud_Data.csv')

print("Columns in dataset:", fraud_df.columns.tolist())

# Flask API Endpoints
@server.route('/api/summary')
def get_summary():
    total = len(fraud_df)
    fraud_cases = fraud_df['class'].sum()
    fraud_percent = (fraud_cases / total) * 100
    return jsonify({
        'purchase_time': total,
        'class': fraud_cases,
        'fraud_percent': round(fraud_percent, 2)
    })



@server.route('/api/trends')
def get_trends():
    trends = fraud_df[fraud_df['class'] == 1].groupby(
        pd.Grouper(key='purchase_time', freq='D')
    ).size().reset_index(name='count')
    return jsonify(trends.to_dict(orient='records'))

@server.route('/api/geography')
def get_geography():
    geo = fraud_df[fraud_df['class'] == 1]['country'].value_counts().reset_index()
    geo.columns = ['country', 'count']
    return jsonify(geo.to_dict(orient='records'))

@server.route('/api/devices')
def get_devices():
    devices = fraud_df[fraud_df['class'] == 1]['source'].value_counts().reset_index()
    devices.columns = ['device', 'count']
    return jsonify(devices.to_dict(orient='records'))

@server.route('/api/browsers')
def get_browsers():
    browsers = fraud_df[fraud_df['class'] == 1]['browser'].value_counts().reset_index()
    browsers.columns = ['browser', 'count']
    return jsonify(browsers.to_dict(orient='records'))

# Dash Layout
app.layout = html.Div([
    html.H1("Fraud Analytics Dashboard", style={'textAlign': 'center'}),
    
    # Summary Cards
    html.Div(id='summary-cards', className='row'),
    
    # Trend Chart
    dcc.Graph(id='trend-chart'),
    
    # Geography and Device Charts
    html.Div(className='row', children=[
        dcc.Graph(id='geo-chart', className='six columns'),
        dcc.Graph(id='device-chart', className='six columns')
    ]),
    
    # Browser Chart
    dcc.Graph(id='browser-chart'),
    
    # Refresh Interval
    dcc.Interval(id='refresh', interval=60*1000)
])

# Callbacks
import requests
@app.callback(
    Output('summary-cards', 'children'),
    Input('refresh', 'n_intervals')
)
def update_summary(_):
     response = requests.get('http://127.0.0.1:5000/api/summary')  # Make sure Flask backend is running
     if response.status_code == 200:
        summary = response.json()
        cards = [
            create_card("Total Transactions", summary['purchase_time'], "#3498db"),
            create_card("Fraud Cases", summary['class'], "#e74c3c"),
            create_card("Fraud Percentage", f"{summary['fraud_percent']}%", "#2ecc71")
        ]
        return cards
     else:
        return ['Error fetching data']
def create_card(title, value, color):
    return html.Div(className='four columns', children=[
        html.Div(className='card', style={'backgroundColor': color}, children=[
            html.H3(title, style={'color': 'white'}),
            html.H2(value, style={'color': 'white'})
        ])
    ])

@app.callback(
    Output('trend-chart', 'figure'),
    Input('refresh', 'n_intervals')
)
def update_trend(_):
    data = get_trends().json
    df = pd.DataFrame(data)
    fig = px.line(df, x='purchase_time', y='count', 
                 title="Fraud Cases Over Time",
                 labels={'count': 'Fraud Cases', 'purchase_time': 'Date'})
    fig.update_layout(plot_bgcolor='white')
    return fig

@app.callback(
    Output('geo-chart', 'figure'),
    Input('refresh', 'n_intervals')
)
def update_geo(_):
    data = get_geography().json
    df = pd.DataFrame(data)
    fig = px.choropleth(df, locations='country', locationmode='country names',
                        color='count', hover_name='country',
                        title="Geographic Distribution of Fraud",
                        color_continuous_scale='Bluered')
    return fig

@app.callback(
    Output('device-chart', 'figure'),
    Input('refresh', 'n_intervals')
)
def update_devices(_):
    data = get_devices().json
    df = pd.DataFrame(data)
    fig = px.bar(df, x='device', y='count', 
                title="Fraud by Device Type",
                color='device')
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output('browser-chart', 'figure'),
    Input('refresh', 'n_intervals')
)
def update_browsers(_):
    data = get_browsers().json
    df = pd.DataFrame(data)
    fig = px.pie(df, names='browser', values='count', 
                title="Fraud by Browser")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)