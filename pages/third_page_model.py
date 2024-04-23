import dash
from dash import Input, Output, State, html, dcc,callback ,dash_table, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time, timedelta
import time as time_pck
import os
import dash_daq as daq
import joblib  # Import joblib to load the trained model



dash.register_page(__name__, path='/model', name='Model')

pipeline_loaded = joblib.load(r'pages/model_pipeline.joblib')



# Define custom styles
custom_button_style = {
    'background-color': '#f0f0f0',
    'border-radius': '10px',
    'padding': '10px',
    'margin-bottom': '5px',
    'text-decoration': 'none',
    'display': 'inline-block',
}
title_style = {
    'font-size': '35px',
    'font-weight': '700',  # Adjust font weight as needed (400 to 700)
    'color': '#0288D1',  # Adjust text color as needed
    'font-family': 'Dancing Script, cursive',  # Specify custom font
}


Div_style = {
    'padding': '20px',
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
    'marginTop': '10px',
    'backgroundColor': 'white',
    'color': '#0288D1',
    'borderRadius': '25px',
    'display': 'flex',
    'justifyContent': 'space-between',  # Align divs horizontally
}

# App layout
layout =html.Div(

    [
        html.Div([

            html.Div([
                html.Img(
                    src="https://i.gifer.com/82by.gif",
                    style={'height': '100px', 'width': 'auto', 'border-radius': '15px', 'margin-right': '10px'}
                ),
                dbc.Label(
                    "Explore Your Obesity Type",
                    style={'font-size': '35px', 'font-weight': '500', 'color': '#0288D1',
                           'font-family': 'Dancing Script, cursive'}
                )
            ], style={'display': 'flex', 'align-items': 'center'}),

            ## first Div with drop down
            html.Div([
                html.Div([
                    # Gender Label and Dropdown Div
                    html.Div([
                        dbc.Label("Gender ♂ ♀", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='gender-dropdown',
                            options=[
                                {'label': 'Female', 'value': 'Female'},
                                {'label': 'Male', 'value': 'Male'}
                            ],
                            value='Female',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'})

                ,

                html.Div([
                    # Age Label and Input Div
                    html.Div([
                        dbc.Label("Age 🎂", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above input

                    html.Div([
                        dcc.Input(id='age-input', type='number', placeholder='Enter Age'),
                    ], style={'width': '100%','padding': '5px 0px 0px  0px'}),  # Input field below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0px 40px'}),

                html.Div([
                    # Height Label and Input Div
                    html.Div([
                        dbc.Label("Height 📏", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above input

                    html.Div([
                        dcc.Input(id='height-input', type='number', placeholder='Enter Height'),
                    ], style={'width': '100%','padding': '5px 0px 0px  0px'}),  # Input field below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'})

                ,

                html.Div([
                    # Weight Label and Input Div
                    html.Div([
                        dbc.Label("Weight ⚖️", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above input

                    html.Div([
                        dcc.Input(id='weight-input', type='number', placeholder='Enter Weight'),
                    ], style={'width': '100%','padding': '5px 0px 0px  0px'}),  # Input field below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'})


            ],className='row' ,style=Div_style)
            ,
            # second Div with items
            html.Div([
                html.Div([
                    # Overweight Family History Label and Dropdown Div
                    html.Div([
                        dbc.Label("Overweight Family History 👩‍🦳", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='overweight-dropdown',
                            options=[
                                {'label': 'yes', 'value': 'yes'},
                                {'label': 'no', 'value': 'no'}
                            ],
                            value='no',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Consumption of Calorie Label and Dropdown Div
                    html.Div([
                        dbc.Label("Consumption of Calorie 🍲", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='calorie-dropdown',
                            options=[
                                {'label': 'yes', 'value': 'yes'},
                                {'label': 'no', 'value': 'no'}
                            ],
                            value='no',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Vegetable Consumption Label and Slider Div
                    html.Div([
                        dbc.Label("Vegetable Consumption 🥦🍆🍑", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above slider

                    html.Div([
                        dcc.Slider(id='vegetable-slider', min=1, max=3, step=1, value=2.0),
                    ], style={'width': '100%'}),  # Slider below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Number of Main Meals Label and Slider Div
                    html.Div([
                        dbc.Label("Number of Main Meals 🍱", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above slider

                    html.Div([
                        dcc.Slider(id='meals-slider', min=1, max=4, step=1, value=2),
                    ], style={'width': '100%'}),  # Slider below label
                ], className='two columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),
            ], className='row', style=Div_style)
            ,

            # third div with items
            html.Div([
                html.Div([
                    # Intermeal Consumption Label and Dropdown Div
                    html.Div([
                        dbc.Label("Intermeal Consumption 🍽️", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='intermeal-dropdown',
                            options=[
                                {'label': 'Always', 'value': 'Always'},
                                {'label': 'Sometimes', 'value': 'Sometimes'},
                                {'label': 'Frequently', 'value': 'Frequently'},
                                {'label': 'no', 'value': 'no'}
                            ],
                            value='Always',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Smoke Label and Dropdown Div
                    html.Div([
                        dbc.Label("Smoke 🚭", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='smoke-dropdown',
                            options=[
                                {'label': 'yes', 'value': 'yes'},
                                {'label': 'no', 'value': 'no'}
                            ],
                            value='no',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Consumption of Water Daily Label and Slider Div
                    html.Div([
                        dbc.Label("Consumption of Water Daily 🥛", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above slider

                    html.Div([
                        dcc.Slider(id='water-slider', min=1, max=3, step=1, value=2.0),
                    ], style={'width': '100%'}),  # Slider below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Calorie Monitoring Label and Dropdown Div
                    html.Div([
                        dbc.Label("Calorie Monitoring 📊", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='calorie-monitoring-dropdown',
                            options=[
                                {'label': 'yes', 'value': 'yes'},
                                {'label': 'no', 'value': 'no'}
                            ],
                            value='no',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),
            ], className='row', style=Div_style)

            ,# fourth div
            html.Div([
                html.Div([
                    # Physical Activity Frequency Label and Slider Div
                    html.Div([
                        dbc.Label("Physical Activity Frequency 🏋️‍♂️",
                                  style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above slider

                    html.Div([
                        dcc.Slider(id='activity-slider', min=0, max=3, step=1, value=2.0),
                    ], style={'width': '100%'}),  # Slider below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Time Technology Devices Label and Slider Div
                    html.Div([
                        dbc.Label("Time Technology Devices ⌚", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above slider

                    html.Div([
                        dcc.Slider(id='technology-slider', min=0, max=2, step=1, value=2.0),
                    ], style={'width': '100%'}),  # Slider below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Consumption of Alcohol Label and Dropdown Div
                    html.Div([
                        dbc.Label("Consumption of Alcohol 🍷", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='alcohol-dropdown',
                            options=[
                                {'label': 'Sometimes', 'value': 'Sometimes'},
                                {'label': 'Frequently', 'value': 'Frequently'},
                                {'label': 'Always', 'value': 'Always'},
                                {'label': 'no', 'value': 'no'}
                            ],
                            value="Sometimes",
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),

                html.Div([
                    # Transportation Used Label and Dropdown Div
                    html.Div([
                        dbc.Label("Transportation Used 🚗", style={'font-family': 'Dancing Script, cursive'}),
                    ], style={'width': '100%', 'text-align': 'left', 'margin-bottom': '5px'}),  # Label above dropdown

                    html.Div([
                        dcc.Dropdown(
                            id='transportation-dropdown',
                            options=[
                                {'label': 'Public_Transportation', 'value': 'Public_Transportation'},
                                {'label': 'Automobile', 'value': 'Automobile'},
                                {'label': 'Walking', 'value': 'Walking'},
                                {'label': 'Motorbike', 'value': 'Motorbike'},
                                {'label': 'Bike', 'value': 'Bike'}
                            ],
                            value='Bike',
                        ),
                    ], style={'width': '100%'}),  # Dropdown field below label
                ], className='three columns', style={'display': 'inline-block', 'width': '25%', 'padding': '0 10px'}),
            ], className='row', style=Div_style)
            ,
            # submmit  Button
            html.Div(
                [
                    dbc.Button(
                        "Submit",
                        id="submit-button",
                        color='#0288D1',
                        className="mt-3",
                        style={
                            'paddingBottom': '5px',
                            "justify-content": "center",  # Align the content horizontally (center)
                            'marginTop': '20px',
                            'marginBottom': '20px',
                            "display": "flex",
                            "width": "15rem",
                            'padding': '10px',
                            'border-radius': '50px',
                            'height': '7vh',
                            'backgroundColor': 'white',
                            'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                            'textAlign': 'center',  # Align the text in the center
                            'font-family': 'Dancing Script, cursive',  # Specify custom font
                            'color': '#0288D1'  # Set the text color
                        }
                    )
                ],
                className='row'
            ),
            # Output div for displaying predictions
            html.Div(
                id='prediction-output',
                className='row'
                # style={'padding': '20px','backgroundColor': 'white' ,'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)', 'border-radius': '15px'}
            )
        ]
                 ,className="nine columns", style={'padding': '20px', 'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                                                'marginTop': '10px', 'backgroundColor': '#E1F5FE',
                                                'color': 'black','borderRadius': '25px'})
] ,style={'paddingLeft':'18rem' ,'paddingRight':'5rem'})





weight_advice = {
    "Insufficient_Weight": "You are underweight 🥺. It's important to maintain a balanced diet and consider consulting with a healthcare professional.",
    "Normal Weight": "Congratulations! You are within a healthy weight range 🎉. Continue to maintain a balanced diet and regular physical activity.",
    "Obesity Type I": "You are classified as obese type I🙄. It's essential to adopt a healthier lifestyle, including dietary changes and regular exercise. Consult with a healthcare professional for personalized advice.",
    "Obesity Type II": "You are classified as obese type II 😒. Immediate action is necessary to address your weight. Consider consulting with a healthcare professional to develop a personalized plan.",
    "Obesity Type III": "You are classified as obese type III 😫. This is a severe health condition requiring urgent attention. Please consult with a healthcare professional immediately.",
    "Overweight Level I": "You are classified as overweight level I 😬. It's important to make lifestyle changes to reduce your weight and improve your health. Consider consulting with a healthcare professional for guidance.",
    "Overweight Level II": "You are classified as overweight level II 🤯. This indicates a higher risk of health problems. It's crucial to take action to reduce your weight. Consult with a healthcare professional for support and advice."
}


@callback(
    Output('prediction-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('gender-dropdown', 'value'),
    State('age-input', 'value'),
    State('height-input', 'value'),
    State('weight-input', 'value'),
    State('overweight-dropdown', 'value'),
    State('calorie-dropdown', 'value'),
    State('vegetable-slider', 'value'),
    State('meals-slider', 'value'),
    State('intermeal-dropdown', 'value'),
    State('smoke-dropdown', 'value'),
    State('water-slider', 'value'),
    State('calorie-monitoring-dropdown', 'value'),
    State('activity-slider', 'value'),
    State('technology-slider', 'value'),
    State('alcohol-dropdown', 'value'),
    State('transportation-dropdown', 'value')
)
def update_prediction(n_clicks, gender, age, height, weight, overweight_history, calorie_consumption, vegetable_consumption,
                      meals_per_day, intermeal_consumption, smoke, water_consumption, calorie_monitoring,
                      physical_activity, technology_usage, alcohol_consumption, transportation_used):
    if n_clicks is None:
        return None

    # Create DataFrame from input data
    data = pd.DataFrame({
        'Gender': [gender],
        'Age': [age],
        'Height': [height],
        'Weight': [weight],
        'family_history_with_overweight': [overweight_history],
        'FAVC': [calorie_consumption],
        'FCVC': [vegetable_consumption],
        'NCP': [meals_per_day],
        'CAEC': [intermeal_consumption],
        'SMOKE': [smoke],
        'CH2O': [water_consumption],
        'SCC': [calorie_monitoring],
        'FAF': [physical_activity],
        'TUE': [technology_usage],
        'CALC': [alcohol_consumption],
        'MTRANS': [transportation_used]
    })


    preprocessed_data = pipeline_loaded.named_steps['preprocessor'].transform(data)
    # Make prediction using the model
    predicted_value = pipeline_loaded.predict(data)
    vale_without_underscore =predicted_value[0].replace("_", " ")
    advice = weight_advice.get(vale_without_underscore, None)

    return html.Div([
        html.Div(f"Your Obesity Type ✍️ ", style=title_style),
        html.Div(vale_without_underscore , style={
                                                                'font-size': '15px',
                                                                'font-weight': '300',
                                                                'color': '#00838F',
                                                                'font-family': 'Dancing Script, cursive',
                                                            }),

        # html.Div("Advice:", style=title_style),
        html.Div(advice, style={
                                                                'font-size': '15px',
                                                                'font-weight': '300',
                                                                'color': '#00838F',
                                                                'font-family': 'Dancing Script, cursive',
                                                            })

    ],style={'padding': '20px','backgroundColor': 'white' ,'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)', 'border-radius': '15px'})
