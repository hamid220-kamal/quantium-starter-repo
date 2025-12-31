"""
Soul Foods Pink Morsel Sales Visualizer
Dash application with region filtering and custom styling.
"""

import dash
from dash import dcc, html, callback, Input, Output
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

# Custom CSS styles
styles = {
    'container': {
        'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        'background': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
        'minHeight': '100vh',
        'padding': '40px 20px'
    },
    'header': {
        'textAlign': 'center',
        'color': '#FF69B4',
        'fontSize': '2.5rem',
        'fontWeight': 'bold',
        'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
        'marginBottom': '10px',
        'letterSpacing': '2px'
    },
    'subtitle': {
        'textAlign': 'center',
        'color': '#e94560',
        'fontSize': '1.2rem',
        'marginBottom': '30px',
        'fontWeight': '300'
    },
    'card': {
        'backgroundColor': 'rgba(255, 255, 255, 0.05)',
        'borderRadius': '20px',
        'padding': '30px',
        'margin': '0 auto',
        'maxWidth': '1400px',
        'boxShadow': '0 8px 32px rgba(0, 0, 0, 0.3)',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'backdropFilter': 'blur(10px)'
    },
    'radioContainer': {
        'display': 'flex',
        'justifyContent': 'center',
        'marginBottom': '25px',
        'padding': '20px',
        'backgroundColor': 'rgba(255, 105, 180, 0.1)',
        'borderRadius': '15px',
        'border': '1px solid rgba(255, 105, 180, 0.3)'
    },
    'radioLabel': {
        'color': '#ffffff',
        'fontSize': '1.1rem',
        'fontWeight': '600',
        'marginRight': '20px',
        'display': 'flex',
        'alignItems': 'center'
    },
    'footer': {
        'textAlign': 'center',
        'color': 'rgba(255, 255, 255, 0.5)',
        'marginTop': '30px',
        'fontSize': '0.9rem'
    }
}

# Define the app layout
app.layout = html.Div([
    # Header Section
    html.Div([
        html.H1('🍬 Soul Foods', style=styles['header']),
        html.H2('Pink Morsel Sales Visualizer', style={
            'textAlign': 'center',
            'color': '#ffffff',
            'fontSize': '1.8rem',
            'fontWeight': '400',
            'marginBottom': '5px'
        }),
        html.P('Analyzing Sales Before and After the Price Increase on January 15, 2021',
               style=styles['subtitle'])
    ]),
    
    # Main Card
    html.Div([
        # Radio Button Filter
        html.Div([
            html.Label('🌍 Filter by Region:', style=styles['radioLabel']),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': ' All Regions', 'value': 'all'},
                    {'label': ' North', 'value': 'north'},
                    {'label': ' South', 'value': 'south'},
                    {'label': ' East', 'value': 'east'},
                    {'label': ' West', 'value': 'west'}
                ],
                value='all',
                inline=True,
                style={'display': 'flex', 'gap': '25px'},
                labelStyle={
                    'color': '#ffffff',
                    'fontSize': '1rem',
                    'cursor': 'pointer',
                    'padding': '8px 16px',
                    'borderRadius': '8px',
                    'transition': 'all 0.3s ease'
                },
                inputStyle={
                    'marginRight': '8px',
                    'accentColor': '#FF69B4'
                }
            )
        ], style=styles['radioContainer']),
        
        # Line Chart
        dcc.Graph(
            id='sales-line-chart',
            style={'height': '550px'},
            config={'displayModeBar': True, 'displaylogo': False}
        )
    ], style=styles['card']),
    
    # Footer
    html.Div([
        html.P('📊 Data Analysis Dashboard | Soul Foods © 2024')
    ], style=styles['footer'])
    
], style=styles['container'])


@callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df.copy()
        chart_title = 'All Regions - Daily Sales'
        line_color = '#FF69B4'
    else:
        filtered_df = df[df['Region'] == selected_region].copy()
        chart_title = f'{selected_region.capitalize()} Region - Daily Sales'
        # Different colors for each region
        region_colors = {
            'north': '#00D4FF',
            'south': '#FFD700',
            'east': '#00FF88',
            'west': '#FF6B6B'
        }
        line_color = region_colors.get(selected_region, '#FF69B4')
    
    # Aggregate sales by date
    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    
    # Convert dates to strings for plotly
    dates = daily_sales['Date'].dt.strftime('%Y-%m-%d').tolist()
    sales = daily_sales['Sales'].tolist()
    
    # Create the figure
    fig = go.Figure()
    
    # Add line trace with gradient fill
    fig.add_trace(go.Scatter(
        x=dates,
        y=sales,
        mode='lines',
        name='Daily Sales',
        line=dict(color=line_color, width=2.5),
        fill='tozeroy',
        fillcolor=f'rgba({int(line_color[1:3], 16)}, {int(line_color[3:5], 16)}, {int(line_color[5:7], 16)}, 0.1)'
    ))
    
    # Add vertical line for price increase date
    fig.add_shape(
        type="line",
        x0='2021-01-15',
        x1='2021-01-15',
        y0=0,
        y1=1,
        yref='paper',
        line=dict(color="#e94560", width=3, dash="dash")
    )
    
    # Add annotation for price increase
    fig.add_annotation(
        x='2021-01-15',
        y=1.05,
        yref='paper',
        text="📍 Price Increase (Jan 15, 2021)",
        showarrow=False,
        font=dict(color="#e94560", size=13, family="Segoe UI"),
        bgcolor="rgba(233, 69, 96, 0.2)",
        bordercolor="#e94560",
        borderwidth=1,
        borderpad=6
    )
    
    # Update layout with dark theme
    fig.update_layout(
        title=dict(
            text=chart_title,
            font=dict(size=20, color='#ffffff', family='Segoe UI'),
            x=0.5
        ),
        xaxis=dict(
            title='Date',
            titlefont=dict(color='#ffffff', size=14),
            tickfont=dict(color='rgba(255,255,255,0.7)', size=11),
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Total Sales ($)',
            titlefont=dict(color='#ffffff', size=14),
            tickfont=dict(color='rgba(255,255,255,0.7)', size=11),
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zeroline=False
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=40, t=80, b=60),
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(0,0,0,0.3)'
        )
    )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
