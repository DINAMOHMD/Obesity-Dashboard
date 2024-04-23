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

# Define the layout of the Dash app
layout =html.Div (
    [
    html.Div([
    # Title section
    html.Div([
        html.H1("Features Impact on Obesity",

    style={'textAlign': 'left', 'marginBottom': '20px',
           'font-size': '35px', 'font-weight': '500', 'color': '#0288D1',
                           'font-family': 'Dancing Script, cursive'})
    ]),
    
    # First part: Dropdown to select a feature and corresponding count plot
    html.Div([
        html.Div([
            html.H4("NObeyesdad vs Categorical Features", style={'marginLeft': '20px', 'font-size': '20px', 'font-weight': '500',
                                           'color': '#01579B', 'font-family': 'Dancing Script, cursive'}),  # Left side title
            html.Div("Select a Feature",   style={'textAlign': 'center', 'marginBottom': '10px', 'font-size': '15px',
                                           'font-weight': '500', 'color': '#01579B', 'font-family': 'Dancing Script, cursive'}),
            dcc.Dropdown(
                id='feature-dropdown',
                options=[{'label': col, 'value': col} for col in cat_columns],
                value=cat_columns[0],
                style={'width': '95%', 'margin': 'auto', 'display': 'block', 'fontSize': '15px'}
            ),
            dcc.Graph(id='feature-countplot')
        ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'marginBottom': '20px', 'padding': '20px'})  # Box style
    ], style={'width': '70%', 'margin': 'auto'}),  # Set the width and margin

    # Second part: Dropdown to select a mobility type and corresponding bar chart
    html.Div([
        html.Div([
            html.H4("NObeyesdad vs Mobility Type", style={'marginLeft': '20px','font-size': '20px', 'font-weight': '500',  'color': '#01579B',
                           'font-family': 'Dancing Script, cursive'}),  # Left side title
            html.Div("Select a Mobility Type", style={'textAlign': 'center', 'marginBottom': '10px','font-size': '20px', 'font-weight': '500',  'color': '#01579B',
                           'font-family': 'Dancing Script, cursive'}),
            dcc.Dropdown(
                id='mobility-dropdown',
                options=[
                    {'label': 'Public Transportation', 'value': 'Public_Transportation'},
                    {'label': 'Automobile', 'value': 'Automobile'},
                    {'label': 'Walking', 'value': 'Walking'},
                    {'label': 'Motorbike', 'value': 'Motorbike'},
                    {'label': 'Bike', 'value': 'Bike'}
                ],
                value='Public_Transportation',
                placeholder="Select a mobility type",
                style={'width': '95%', 'margin': 'auto', 'display': 'block', 'fontSize': '15px'}
            ),
            dcc.Graph(id='mobility-graph')
        ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'padding': '20px'})  # Box style
    ], style={'width': '70%', 'margin': 'auto'})  # Set the width and margin
])
],style={'paddingLeft':'17rem'})

# Callback to update the count plot based on selected feature
@callback(
    Output('feature-countplot', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_countplot(selected_feature):
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
        
        layout = go.Layout(title=f'Countplot of Obesity Types by {selected_feature}',
                           xaxis={'title': 'Obesity Types'},
                           yaxis={'title': 'Count'},
                           barmode='group')
        
        return {'data': data, 'layout': layout}
    else:
        return {}

# Callback to update the bar chart based on selected mobility type
@callback(
    Output('mobility-graph', 'figure'),
    [Input('mobility-dropdown', 'value')]
)
def update_graph(selected_mobility):
    filtered_data = train[train['MTRANS'] == selected_mobility]['NObeyesdad'].value_counts().sort_index().reset_index()
    filtered_data.columns = ['NObeyesdad', 'count']
    total_count = filtered_data['count'].sum()
    filtered_data['percentage'] = (filtered_data['count'] / total_count) * 100
    colors = [color_map.get(x, 'rgba(0, 0, 0, 0.7)') for x in filtered_data['NObeyesdad']]
    fig = px.bar(filtered_data, x='NObeyesdad', y='count', color='NObeyesdad', color_discrete_sequence=colors,
                 labels={'NObeyesdad': 'Weight Category', 'count': 'Count'}, title=f'{selected_mobility} vs Weight Category Distribution')
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'}, xaxis={'title': 'Weight Category'}, yaxis={'title': 'Count'})

    # Add percentage labels above bars
    for i, row in filtered_data.iterrows():
        if row['NObeyesdad'] in ['Motorbike', 'Bike']:
            y_shift = 10  # Adjust the vertical shift for 'Motorbike' and 'Bike'
        else:
            y_shift = 5  # Default vertical shift
        fig.add_annotation(
            x=row['NObeyesdad'],
            y=row['count'] + 0.5,  # Adjust the position of the label above the bar
            text=f"{row['percentage']:.2f}%",
            showarrow=False,
            font=dict(size=10),
            yshift=y_shift  # Offset the label vertically
        )

    return fig
