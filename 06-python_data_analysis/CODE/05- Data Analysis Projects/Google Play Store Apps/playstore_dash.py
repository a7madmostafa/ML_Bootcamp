from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Load and preprocess dataset
df = pd.read_csv('playstore_cleaned.csv')

# Initialize the app
app = Dash(__name__)

# Explore Numerical Features
def explore_numerical(feature):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Histogram', 'Boxplot'))
    fig.add_trace(go.Histogram(x=df[feature], name='Histogram'), row=1, col=1)
    fig.add_trace(go.Box(y=df[feature], name='Boxplot'), row=1, col=2)
    fig.update_layout(title_text=f'Exploratory Analysis of {feature}', showlegend=False)
    return fig

# Explore Categorical Features
def explore_categorical(feature):
    fig = px.bar(df, x=feature, title=f'Exploratory Analysis of {feature}', color_discrete_sequence=['#1f77b4'])
    return fig

# App layout
app.layout = html.Div(style={'backgroundColor': '#e0f7fa'}, children=[
    html.H1(
        "Google Playstore Apps Dashboard",
        style={
            'textAlign': 'center',
            'color': '#0277bd',
            'font-family': 'Arial',
            'backgroundColor': '#81d4fa',
            'padding': '20px'
        }
    ),
    dcc.Markdown('''
        This dashboard provides an exploratory analysis of the Google Playstore Apps dataset.    
        You can explore different features by selecting from the dropdown menu below.   
        Source: [Kaggle](https://www.kaggle.com/lava18/google-play-store-apps)
                 ''',
        style={'textAlign': 'center', 'font-family': 'Arial', 'padding': '20px'}
    ),
    dcc.Dropdown(
        id='feature-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype in ['object', 'int64', 'float64']],
        placeholder='Select a feature to explore',
        style={'width': '50%', 'margin': '0 auto'}
    ),
    dcc.Graph(id='feature-graph')
])

# Callback to update graph based on selected feature
@callback(
    Output('feature-graph', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_graph(selected_feature):
    if selected_feature is None:
        return {}
    elif df[selected_feature].dtype in ['int64', 'float64']:
        return explore_numerical(selected_feature)
    else:
        return explore_categorical(selected_feature)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
