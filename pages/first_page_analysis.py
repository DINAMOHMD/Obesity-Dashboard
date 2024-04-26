# Import Libraries
import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff

dash.register_page(__name__, path='/', name='Analysis')

# Read Data 
df = pd.read_csv(r'data/train.csv')

# Preprocessing for columns
df['Age'] = df['Age'].astype(int)
df[['Height', 'Weight', 'CH2O']] = df[['Height', 'Weight', 'CH2O']].round(2)
df[['FCVC', 'NCP', 'TUE', 'FAF']] = df[['FCVC', 'NCP', 'TUE', 'FAF']].round().astype(int)

# Cards for SMOKE
num_non_smokers = df['SMOKE'].value_counts()['no']
num_smokers = df['SMOKE'].value_counts()['yes']

smoke_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3(children=[html.I(className="bi bi-fire me-2"), "Non Smokers"], className="text-nowrap"),
            html.H4(num_smokers),
        ], className="border-start border-danger border-5"
    ),
    className="text-center m-4",
)

non_smoke_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3(children=[html.I(className="bi bi-fire me-2"), "Smokers"], className="text-nowrap"),
            html.H4(num_non_smokers),
        ], className="border-start border-success border-5"
    ),
    className="text-center m-4",
)

# Cards for Gender
num_male = df['Gender'].value_counts()['Male']
num_female = df['Gender'].value_counts()['Female']

male_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3([html.I(className="bi bi-gender-male me-2"), "Male"], className="text-nowrap"),
            html.H4(num_male),
        ], className="border-start border-info border-5"
    ),
    className="text-center m-4",
)

female_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3([html.I(className="bi bi-gender-female me-2"), "Female"], className="text-nowrap"),
            html.H4(num_female),
        ], className="border-start border-danger border-5"
    ),
    className="text-center m-4",
)

# Function For Weight
# Group data by frequency of consuming vegetables and calculate average weight
grouped_data1 = df.groupby('FCVC')['Weight'].mean().reset_index()

# Calculate percentages
total_count = df['FCVC'].count()
grouped_data1['Percentage'] = (grouped_data1['Weight'] / total_count) * 100





# Create bar plot
fig1 = go.Figure(data=[go.Bar(
x = grouped_data1['FCVC'],
y = grouped_data1['Weight'],
text = grouped_data1['Percentage'].round(2).astype(str) + '%',
textposition = 'outside',
marker=dict(color='#4FC3F7')
)])


# Add labels and title
fig1.update_layout(
xaxis=dict(
        title='Frequency of Consuming Vegetables',
        tickvals=[1, 2, 3],  # Original values
        ticktext=['Low', 'Medium', 'High']  # Custom labels corresponding to those values
    ),
    yaxis=dict(
        title='Average Weight'
    )
)

# Function For Physical Activity and Transportation 
# Group data by physical activity and transportation, and count occurrences
grouped_data3 = df.groupby(['FAF', 'MTRANS']).size().unstack(fill_value=0)

# Create stacked bar chart
fig3 = go.Figure()

custom_x_labels = ['Very low', 'Low', 'Medium', 'High']
x_values = list(range(len(custom_x_labels)))

for activity in grouped_data3.columns:
    fig3.add_trace(go.Bar(
        x=x_values,  # Use index to associate with custom labels
        y=grouped_data3[activity],  # Corresponding data
        name=activity
    ))
    
# Add labels and title
fig3.update_layout(
    title='Physical Activity vs Transportation',
    xaxis=dict(
        title='Physical Activity',
        tickvals=list(range(len(custom_x_labels))),  # Indices corresponding to custom labels
        ticktext=custom_x_labels  # Custom labels for x-axis
    ),
    title_font_color='#01579B',
    yaxis=dict(title='Count'),
    barmode='stack'
)


layout = html.Div(children=[
    # Title
    html.H1("Obesity Analysis",style={'font-size': '35px', 'font-weight': '500', 'color': '#0288D1',
                           'font-family': 'Dancing Script, cursive'} ,className="text-left"),
    
    # Cards
    dbc.Row(
        [dbc.Col(smoke_card), 
         dbc.Col(non_smoke_card), 
         dbc.Col(male_card), 
         dbc.Col(female_card)],
        
    ),
    
    # 2 Graphs
    dbc.Row([
        # First Graph For Continous Columns (Age, Weight)
        dbc.Col(
            html.Div([
            html.H4("Split Continous Feature into Categories", style={'marginLeft': '20px', 'font-size': '20px', 'font-weight': '500',  'color': '#01579B',
                           'font-family': 'Dancing Script, cursive'}),  # Left side title
            html.Div("Select a Feature", style={'textAlign': 'center', 'marginTop': '10px'  ,'marginBottom': '10px', 'font-size': '20px', 'font-weight': '500', 'color': '#01579B','font-family': 'Dancing Script, cursive'}),
            dcc.Dropdown(
            id='continous-dropdown',
            options=[
                {'label': 'Weight', 'value': 'Weight'},
                {'label': 'Age', 'value': 'Age'}
            ],
            value='Weight'  # Default value
            ),
            dcc.Graph(id='histogram-graph')
        ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'marginBottom': '20px', 'padding': '20px', 'width': '600px'})
        ),
        
        # Second Graph For The Relationship between (FCVC, SCC), (FCVC, Weight)
        dbc.Col(
            html.Div([
                html.H4("Average Weight by Vegetable Frequency Consumption", style={'marginLeft': '20px','font-size': '20px', 'font-weight': '500', 'color': '#01579B','font-family': 'Dancing Script, cursive'}),
                dcc.Graph(figure=fig1,style={'width': '500px', 'height': '500px'})
                ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'marginBottom': '20px', 'padding': '20px', 'width': '600px', 'height':'600px'})
            ),
        
        # Second Graph For The Relationship between (FCVC, SCC), (FCVC, Weight)
        # dbc.Col(
        #     html.Div([
        #         dcc.Graph(figure=fig1)
        #         ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'marginBottom': '20px', 'padding': '20px'})
        #     )

        ]),
    
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(figure=fig3)
                ], style={'box-shadow': '5px 10px 18px #888888', 'borderRadius': '10px', 'marginBottom': '20px', 'padding': '20px'})
            )

        ])
    
], style={'paddingLeft':'17rem'})


# Callback for continous columns (Age, Weight, Height)
@callback(
    Output('histogram-graph', 'figure'),
    Input('continous-dropdown', 'value')
)


# Function to create a histogram with annotations
def update_graph(selected_data_type):
    colors = ['#E1F5FE', '#4cc9f0', '#29B6F6', '#0091EA', '#039BE5', '#81D4FA']
    
    bins_dict = {
    'Weight': [0, 20, 50, 70, 90, 120, 160, 200],  # Bins for Weight
    'Age': [0, 20, 30, 40, 50, 60, 70, 80, 90]  # Bins for Age
    }

    freq, edges = np.histogram(df[selected_data_type], bins=bins_dict[selected_data_type])
    bin_centers = np.diff(edges) * 0.5 + edges[:-1]

    bar_colors = colors[:len(bin_centers)]

    # Create a bar plot
    fig = go.Figure(
        go.Bar(
            x=bin_centers,
            y=freq,
            width=0.9 * np.diff(edges),
            marker=dict(color=bar_colors)
        )
    )

    # Add annotations for start and end of each bar
    for start, end in zip(edges[:-1], edges[1:]):
        # Annotation for start of the bar
        fig.add_annotation(
            x=start,
            y=0,  # At the baseline
            yshift=-15,  # Slight downward shift
            text=f"{start}",
            showarrow=False,
            font=dict(color='black', size=12)
        )

        # Annotation for end of the bar
        fig.add_annotation(
            x=end,
            y=0,  # At the baseline
            yshift=-15,  # Slight downward shift
            text=f"{end}",
            showarrow=False,
            font=dict(color='black', size=12)
        )

    # Add annotations for percentages above the bars
    for fr, x in zip(freq, bin_centers):
        fig.add_annotation(
            x=x,
            y=fr,
            yshift=10,  # Adjust upwards for better visibility
            text=f"{round(fr * 100 / df[selected_data_type].count(), 2)}%",
            showarrow=False,
            font=dict(color='black', size=12)
        )

    # Update the layout, hiding default x-axis tick labels
    fig.update_layout(
        title=f'{selected_data_type} Distribution',
        xaxis=dict(title=selected_data_type, showticklabels=False),  # Hide default x-axis tick labels
        yaxis=dict(title='Frequency'),
        bargap=0.05  # Gap between bars
    )

    return fig