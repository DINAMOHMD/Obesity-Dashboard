# Import Libraries
import dash
from dash import html, dcc, Dash, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px

# Dash app
app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    'borderRadius': '15px',
    "background-color": '#E1F5FE',
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "0.5rem 1rem",
}

sidebar = html.Div(
    [

        html.Div([
            html.H2([
                html.Img(
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1nuCG1CmDWMYVP_YLvD5dtonxRQAS4FwKx_Er3bp9JoeqgVkq",
                    style={'height': '40px', 'margin-right': '10px','borderRadius': '40%'}),
                "Obesity"
            ], style={
                'display': 'flex',
                'align-items': 'center',  # Align items vertically in the flex container
                'font-size': '35px',
                'font-weight': '700',  # Adjust font weight as needed (400 to 700)
                'color': '#0288D1',  # Adjust text color as needed
                'font-family': 'Dancing Script, cursive',  # Specify custom font
            })
        ], className="display-4")

        ,
        html.Hr(),
        html.P(
            "This Dashboard is estimation of obesity levels for people from Mexico, Peru and Colombia",style={
                    'font-size': '15px',
                    'font-weight': '700',  # Adjust font weight as needed (400 to 700)
                    'color': '#0288D1',  # Adjust text color as needed
                    'font-family': 'Dancing Script, cursive',  # Specify custom font
                }
        ),
        dbc.Nav(
            [
                dbc.NavLink("Obesity Analysis", href="/", active="exact", style={'font-family': 'Dancing Script, cursive'}),
                # Set the color to white
                dbc.NavLink("Features Impact on Obesity", href="/features", active="exact",style={'font-family': 'Dancing Script, cursive'}),
                dbc.NavLink("Obesity Prediction", href="/model", active="exact",style={'font-family': 'Dancing Script, cursive'}),
                dbc.NavLink("GitHub", href="https://github.com/DINAMOHMD/Obesity-Dashboard.git", active="exact",style={'font-family': 'Dancing Script, cursive'},external_link=True  ,target="_blank"),
            ],
            vertical=True,
            pills=True,
            style={'box-shadow': '1px 4px 2px -2px gray'}  # Add shadow on hover
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Dash layout
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
    html.Div(children=[
	    dcc.Link(page['name'], href=page["relative_path"]) for page in dash.page_registry.values()]),
    dash.page_container
])

# Run Server
if __name__=='__main__':
    app.run_server(debug=True, port=3000)
