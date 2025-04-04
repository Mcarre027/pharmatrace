import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.graphs import plot_world_map

dash.register_page(__name__, path="/", name="Accueil")

layout = dbc.Container([
    dbc.Card(
        dbc.CardBody([
            html.H2("Bienvenue sur le tableau de bord de pharmacovigilance", className="mb-4 text-center"),
            html.P(
                "Ce tableau de bord vous permet d'explorer les effets secondaires rapportés "
                "suite à l'administration de vaccins, à partir de données réelles issues d'OpenFDA. "
                "Utilisez les onglets à gauche pour visualiser la heatmap des réactions "
                "et explorer plus en détail les tendances par âge, sexe et région.",
                className="mt-4 text-justify"
            ),
            html.Div(style={"height": "30px"}),
            html.Hr(),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=plot_world_map(), style={"height": "500px"})
                ], width=12),
            ], className="my-4"),

            html.P(
                "Cette carte interactive présente une vue mondiale des pays ayant déclaré des effets secondaires, avec des nuances selon la fréquence des déclarations.",
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
                        html.H4("+600", className="text-success"),
                        html.P("effets secondaires répertoriés.")
                    ], className="chiffre-cle"),

                    html.Div([
                        html.H4("+650", className="text-warning"),
                        html.P("vaccins associés à au moins un effet secondaire.")
                    ], className="chiffre-cle"),
                ], className="chiffres-cles")
            ])
        ]), className="shadow-lg"
    )
], fluid=True, className="mt-5")
