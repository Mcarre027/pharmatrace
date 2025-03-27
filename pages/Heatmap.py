import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from collections import Counter

dash.register_page(__name__, path="/heatmap", name="Heatmap")

# Charger les données
df = load_data()

# Extraire la liste de tous les vaccins uniques
vaccins_uniques = sorted({v for liste in df['vaccine_name'] for v in liste})

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Heatmap des effets secondaires par vaccin", className="mb-4"),
            html.P("Sélectionnez un ou plusieurs vaccins pour afficher la fréquence des effets secondaires."),
            dcc.Dropdown(
                options=[{"label": v, "value": v} for v in vaccins_uniques],
                value=[vaccins_uniques[0]],  # par défaut un vaccin sélectionné
                multi=True,
                id="dropdown-vaccins"
            ),
            dcc.Loading(dcc.Graph(id="heatmap", style={"height": "700px"}), type="default"),
            html.P("""
                Cette heatmap permet de visualiser l’intensité des effets secondaires en fonction des vaccins sélectionnés. 
                Plus la couleur est intense, plus l’effet secondaire est fréquemment rapporté pour ce vaccin. 
                Cela permet d’identifier rapidement les effets spécifiques à certains vaccins ainsi que les tendances générales.
            """, className="mt-4 text-justify")
        ], width=10, className="mx-auto")
    ])
], fluid=True)

# Callback pour mettre à jour la heatmap
@dash.callback(
    Output("heatmap", "figure"),
    Input("dropdown-vaccins", "value")
)
def update_heatmap(vaccin_selection):
    if not vaccin_selection:
        return px.imshow([[0]], labels=dict(x="Effets secondaires", y="Vaccin", color="Fréquence"))

    # Filtrer les données
    df_filtered = df[df['vaccine_name'].apply(lambda x: any(v in x for v in vaccin_selection))]

    # Compter les effets par vaccin
    data = {v: Counter() for v in vaccin_selection}
    for _, row in df_filtered.iterrows():
        for v in row['vaccine_name']:
            if v in vaccin_selection:
                data[v].update(row['reactions'])

    # Construire un DataFrame
    all_effects = sorted({effet for d in data.values() for effet in d})
    heatmap_data = pd.DataFrame(index=vaccin_selection, columns=all_effects).fillna(0)
    for v in vaccin_selection:
        for effet in data[v]:
            heatmap_data.loc[v, effet] = data[v][effet]

    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        labels=dict(x="Effets secondaires", y="Vaccin", color="Fréquence"),
        color_continuous_scale="Plasma"
    )
    fig.update_layout(
        margin=dict(t=40, l=60, r=20, b=150),
        plot_bgcolor='#1e1e2f',
        paper_bgcolor='#1e1e2f'
    )
    return fig
