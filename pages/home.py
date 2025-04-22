import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.graphs import plot_world_map

dash.register_page(__name__, path="/", name="Accueil")

layout = dbc.Container([
    dbc.Card(
        dbc.CardBody([
            html.H2("Bienvenue sur le tableau de bord de pharmacovigilance – PharmaTrace", className="mb-4 text-center"),
            html.P(
                "Ce tableau de bord interactif vous permet d'explorer les effets secondaires rapportés pour des milliers de médicaments, à partir de données réelles issues d'OpenFDA "
                "Utilisez les onglets à gauche pour visualiser la heatmap des réactions et explorer plus en détail les tendances par principe actif, classe thérapeutique, sexe ou tranche d'âge. ",
                className="mt-4 text-justify"
            ),
            html.Div(style={"height": "30px"}),
            html.Hr(),

            dbc.Row([
                dbc.Col([
                    html.Div(
                        dcc.Graph(
                            figure=plot_world_map(), 
                            style={"width": "100%", "height": "450px"},
                            className="centered-plot"
                        ),
                        className="shadow-lg rounded"
                    )
                ], width=12),
            ], className="my-4"),

            html.P(
                "Cette carte interactive présente une vue mondiale des effets indésirables déclarés, avec des nuances selon la fréquence des événements et les médicaments concernés.",
                className="mt-4 text-justify"
            ),

            html.Hr(),
            html.H3("Chiffres clés", className="mt-5 mb-3 text-center"),
            html.Div(style={"height": "30px"}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H4("+30", className="text-primary"),
                        html.P("pays ont signalé des effets secondaires.")
                    ], className="chiffre-cle"),

                    html.Div([
                        html.H4("+1460", className="text-success"),
                        html.P("effets secondaires répertoriés.")
                    ], className="chiffre-cle"),

                    html.Div([
                        html.H4("+2880", className="text-warning"),
                        html.P("médicaments ou principes actifs liés à au moins un effet secondaire.")
                    ], className="chiffre-cle"),
                ], className="chiffres-cles")
            ])
        ]), className="shadow-lg"
    )
], fluid=True, className="mt-5")