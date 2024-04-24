import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

dash.register_page(__name__, path='/features', Name='Features')

# Load your datasets
train_sample = pd.read_csv(r'data/train.csv')
train_orgin_extra = pd.read_csv(r'data/ObesityDataSet.csv')
train = pd.concat([train_sample, train_orgin_extra], ignore_index=True)

# Get categorical columns
cat_columns = train.select_dtypes(include=['object']).columns.tolist()
cat_columns.remove('NObeyesdad')
cat_columns.remove('MTRANS')

# Define color map
color_map = {
    'Insufficient_Weight': 'rgba(31, 119, 180, 0.7)',
    'Normal_Weight': 'rgba(255, 127, 14, 0.7)',
    'Overweight_Level_I': 'rgba(44, 160, 44, 0.7)',
    'Overweight_Level_II': 'rgba(214, 39, 40, 0.7)',
    'Obesity_Type_I': 'rgba(148, 103, 189, 0.7)',
    'Obesity_Type_II': 'rgba(140, 86, 75, 0.7)',
    'Obesity_Type_III': 'rgba(227, 119, 194, 0.7)'
}

# Define feature names
feature_names = {
    'Gender': 'Gender',
    'family_history_with_overweight': 'Family History with Overweight',
    'FAVC': 'Calorie Consumption',
    'CAEC': 'Intermeal Consumption',
    'SMOKE': 'Smoke',
    'SCC': 'Calorie Monitoring',
    'CALC': 'Alcohol Consumption'
}

# Define the layout of the Dash app
layout = html.Div (
    [
        html.Div([
            # Title section
            html.Div([
                html.H1("Features Impact on Obesity",
                    style={'textAlign': 'left', 'marginBottom': '20px',
                           'font-size': '35px', 'font-weight': '500', 'color': '#0288D1',
                           'font-family': 'Dancing Script, cursive'})
            ]),
    
            # First part: Dropdown to select a feature and corresponding plot
            html.Div([
                html.Div([
                    html.H4("NObeyesdad vs Categorical Features", style={'marginLeft': '20px', 'font-size': '20px', 'font-weight': '500',
                                                                       'color': '#01579B', 'font-family': 'Dancing Script, cursive'}),  # Left side title
                    html.Div("Select a Feature",   style={'textAlign': 'center', 'marginBottom': '10px', 'font-size': '15px',
                                                           'font-weight': '500', 'color': '#01579B', 'font-family': 'Dancing Script, cursive'}),
                    dcc.Dropdown(
                        id='feature-dropdown',
                        options=[{'label': feature_names[col], 'value': col} for col in cat_columns],
                        value=cat_columns[0],
                        style={'width': '95%', 'margin': 'auto', 'display': 'block', 'fontSize': '15px'}
                    ),
                    dcc.Graph(id='feature-plot')
                ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'marginBottom': '20px', 'padding': '20px'})  # Box style
            ], style={'width': '70%', 'margin': 'auto'})  # Set the width and margin

        ], style={'paddingLeft':'17rem'})
    ]
)

# Callback to update the plot based on selected feature
@callback(
    Output('feature-plot', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_plot(selected_feature):
    if selected_feature:
        data = []
        unique_values = train[selected_feature].unique()
        color_palette = sns.color_palette('husl', n_colors=len(unique_values)).as_hex()
        for value, color in zip(unique_values, color_palette):
            filtered_data = train[train[selected_feature] == value]['NObeyesdad'].value_counts().sort_index().reset_index()
            filtered_data.columns = ['NObeyesdad', 'count']
            total_count = filtered_data['count'].sum()
            filtered_data['percentage'] = (filtered_data['count'] / total_count) * 100
            trace = go.Bar(x=filtered_data['NObeyesdad'], y=filtered_data['count'], name=str(value), marker_color=color, legendgroup=str(value),
                           text=[f"{perc:.2f}%" for perc in filtered_data['percentage']], textposition='outside', textfont=dict(color='black'))
            data.append(trace)
        
        layout = go.Layout(title=f'Obesity Types Distribution by {feature_names[selected_feature]}',
                           xaxis={'title': 'Obesity Types'},
                           yaxis={'title': 'Count'},
                           barmode='group')
        
        return {'data': data, 'layout': layout}
    else:
        return {}
