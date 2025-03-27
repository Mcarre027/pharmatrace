import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.graphs import plot_world_map

dash.register_page(__name__, path="/", name="Accueil")

layout = dbc.Container([
    dbc.Card(
        dbc.CardBody([
            html.H2("Bienvenue sur le tableau de bord de pharmacovigilance", className="mb-4"),
            html.P(
                "Ce tableau de bord vous permet d'explorer les effets secondaires rapportés "
                "suite à l'administration de vaccins, à partir de données réelles issues d'OpenFDA. "
                "Utilisez les onglets à gauche pour visualiser la heatmap des réactions "
                "et explorer plus en détail les tendances par âge, sexe et région.",
                className="mt-4 text-justify"
            ),
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
            html.H4("Chiffres clés", className="mt-5 mb-3"),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("+30 pays", className="card-title text-primary"),
                        html.P("ont signalé des effets secondaires.", className="card-text")
                    ])
                ]), width=4),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("+600 effets secondaires", className="card-title text-success"),
                        html.P("différents répertoriés dans les déclarations.", className="card-text")
                    ])
                ]), width=4),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("+650 vaccins", className="card-title text-warning"),
                        html.P("associés à au moins un effet secondaire.", className="card-text")
                    ])
                ]), width=4),
            ], className="mt-3")

        ]), className="shadow-lg"
    )
], fluid=True, className="mt-5")
