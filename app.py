import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Effets secondaires des vaccins"

navbar = dbc.NavbarSimple(
    brand=[
        DashIconify(icon="fa-solid:virus", width=24, style={"margin-right": "10px"}),
        html.Span("Effets secondaires des vaccins")
    ],
    brand_href="/",
    color="#1e2130",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Accueil", href="/")),
        dbc.NavItem(dbc.NavLink("Heatmap", href="/heatmap")),
        dbc.NavItem(dbc.NavLink("Exploration", href="/exploration")),
    ],
    className="mb-4"
)

app.layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col(dash.page_container)
    ])
], fluid=True)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)