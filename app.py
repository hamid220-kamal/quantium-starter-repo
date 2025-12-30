"""
Soul Foods Pink Morsel Sales Visualizer
Dash application to visualize sales data and analyze the impact of the price increase on January 15, 2021.
"""

import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the formatted sales data
data_path = os.path.join('data', 'formatted_output.csv')
df = pd.read_csv(data_path)

# Convert Date column to datetime and sort by date
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Aggregate sales by date (sum across all regions)
daily_sales = df.groupby('Date')['Sales'].sum().reset_index()

# Convert dates to list for plotly compatibility
dates = daily_sales['Date'].dt.strftime('%Y-%m-%d').tolist()
sales = daily_sales['Sales'].tolist()

# Create the line chart using graph_objects
fig = go.Figure()

# Add line trace
fig.add_trace(go.Scatter(
    x=dates,
    y=sales,
    mode='lines',
    name='Daily Sales',
    line=dict(color='#FF69B4', width=2)
))

# Add a vertical line to mark the price increase date using shapes
fig.add_shape(
    type="line",
    x0='2021-01-15',
    x1='2021-01-15',
    y0=0,
    y1=1,
    yref='paper',
    line=dict(color="red", width=2, dash="dash")
)

# Add annotation for the price increase date
fig.add_annotation(
    x='2021-01-15',
    y=1,
    yref='paper',
    text="Price Increase (Jan 15, 2021)",
    showarrow=False,
    font=dict(color="red", size=12),
    yshift=10
)

# Update layout for better appearance
fig.update_layout(
    title='Pink Morsel Daily Sales Over Time',
    xaxis_title='Date',
    yaxis_title='Total Sales ($)',
    hovermode='x unified',
    template='plotly_white'
)

# Define the app layout
app.layout = html.Div([
    html.H1(
        'Soul Foods Pink Morsel Sales Visualizer',
        style={
            'textAlign': 'center',
            'color': '#FF69B4',
            'marginBottom': '20px',
            'marginTop': '20px',
            'fontFamily': 'Arial, sans-serif'
        }
    ),
    html.H3(
        'Analyzing Sales Before and After the Price Increase on January 15, 2021',
        style={
            'textAlign': 'center',
            'color': '#666',
            'marginBottom': '30px',
            'fontFamily': 'Arial, sans-serif'
        }
    ),
    dcc.Graph(
        id='sales-line-chart',
        figure=fig,
        style={'height': '600px'}
    )
], style={
    'padding': '20px',
    'backgroundColor': '#f9f9f9',
    'minHeight': '100vh'
})

# Run the app (Dash 3.x uses app.run instead of app.run_server)
if __name__ == '__main__':
    app.run(debug=True)
