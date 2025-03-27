import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialisation de l'app
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

print(dash.page_registry.keys())
app.title = "Effets secondaires des vaccins"

# Layout global
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Effets secondaires des vaccins", className="text-center my-4"))
    ]),
    dbc.Row([
        dbc.Col(dbc.Nav([
            dbc.NavLink("Accueil", href="/", active="exact"),
            dbc.NavLink("Heatmap", href="/heatmap", active="exact"),
            dbc.NavLink("Exploration", href="/exploration", active="exact")
        ], vertical=True, pills=True), width=2),
        dbc.Col(dash.page_container, width=10)
    ])
], fluid=True)

if __name__ == "__main__":
    app.run (debug=True)
