import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from collections import Counter
import io
import base64
from dash import ctx, State

dash.register_page(__name__, path="/heatmap", name="Heatmap")

# Charger les données
df = load_data()

# Extraire la liste de tous les vaccins uniques
vaccins_uniques = sorted({v for liste in df['vaccine_name'] for v in liste})

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(style={"height": "40px"}),
            html.H2("Heatmap des effets secondaires par vaccin", className="mb-4 text-center"),
            html.P("Sélectionnez un ou plusieurs vaccins pour afficher la fréquence des effets secondaires."),
            dcc.Dropdown(
                options=[{"label": v, "value": v} for v in vaccins_uniques],
                value=[vaccins_uniques[0]],
                multi=True,
                id="dropdown-vaccins",
                style={"width": "100%"}
            ),
            html.Div(id="heatmap-stats", className="text-info my-3 text-center"),
            dcc.Loading(
                dcc.Graph(id="heatmap", className="centered-plot", style={"height": "100%", "width": "100%"}),
                type="default"
            ),
            html.Div(id="info-empty", className="text-muted mt-3 text-center"),
            html.P("""
                Cette heatmap permet de visualiser l’intensité des effets secondaires en fonction des vaccins sélectionnés. 
                Plus la couleur est intense, plus l’effet secondaire est fréquemment rapporté pour ce vaccin. 
                Cela permet d’identifier rapidement les effets spécifiques à certains vaccins ainsi que les tendances générales.
            """, className="mt-4 text-justify"),
            html.Div(style={"height": "30px"}),

            html.H3("Tableau des effets secondaires", className="text-center mt-5 mb-3"),
            html.Div(style={"height": "30px"}),
            html.Div(id="table-container", className="mb-4"),
            html.Div(style={"height": "30px"}),
            html.Div([
                html.Button("Exporter en CSV", id="btn-export", className="btn btn-primary my-3"),
                dcc.Download(id="download-dataframe")
            ], className="text-center mb-4"),
            html.Div(style={"height": "30px"}),
            html.H3("Répartition des effets secondaires", className="text-center mt-5 mb-3"),
            html.Div(style={"height": "30px"}),
            html.Div(id="barplot-container")
        ], width=12)
    ])
], fluid=True)

# Callback principal
@dash.callback(
    Output("heatmap", "figure"),
    Output("info-empty", "children"),
    Output("heatmap-stats", "children"),
    Output("table-container", "children"),
    Output("barplot-container", "children"),
    Input("dropdown-vaccins", "value")
)
def update_heatmap(vaccin_selection):
    if not vaccin_selection:
        fig = go.Figure(go.Heatmap(z=[[0]], x=["Effets"], y=["Vaccin"]))
        fig.update_layout(plot_bgcolor="#1e1e2f", paper_bgcolor="#1e1e2f")
        return fig, "Veuillez sélectionner au moins un vaccin.", "", "", ""

    df_filtered = df[df['vaccine_name'].apply(lambda x: any(v in x for v in vaccin_selection))]

    data = {v: Counter() for v in vaccin_selection}
    for _, row in df_filtered.iterrows():
        for v in row['vaccine_name']:
            if v in vaccin_selection:
                data[v].update(row['reactions'])

    all_effects = sorted({effet for d in data.values() for effet in d})
    heatmap_data = pd.DataFrame(index=vaccin_selection, columns=all_effects).fillna(0)

    for v in vaccin_selection:
        for effet in data[v]:
            heatmap_data.loc[v, effet] = data[v][effet]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale="Viridis",
        text=heatmap_data.values,
        texttemplate="%{text}",
        hovertemplate='Vaccin: %{y}<br>Effet: %{x}<br>Fréquence: %{z}<extra></extra>',
        colorbar=dict(title="Fréquence"),
        xgap=2,
        ygap=2
    ))

    fig.update_layout(
        margin=dict(t=20, l=20, r=20, b=20),
        plot_bgcolor='#1e1e2f',
        paper_bgcolor='#1e1e2f',
        font=dict(color='white'),
        height=450,
        title_x=0.5
    )

    fig.update_xaxes(tickangle=-45)

    nb_effets = heatmap_data.shape[1]
    nb_vaccins = len(vaccin_selection)

    table_df = heatmap_data.reset_index().rename(columns={"index": "Vaccin"})
    table = dash_table.DataTable(
        data=table_df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in table_df.columns],
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#1e2130", "color": "white"},
        style_cell={"backgroundColor": "#272b3f", "color": "white", "textAlign": "center", "padding": "5px"}
    )

    total_effects = heatmap_data.sum(axis=0).sort_values(ascending=False).reset_index()
    total_effects.columns = ["Effet secondaire", "Total"]

    piechart = px.pie(
        total_effects.head(10),
        names="Effet secondaire",
        values="Total",
        title="Répartition des 10 effets secondaires les plus fréquents",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    piechart.update_layout(
        plot_bgcolor="#1e1e2f",
        paper_bgcolor="#1e1e2f",
        font=dict(color="white"),
        title_x=0.5
    )

    return fig, "", f"{nb_vaccins} vaccin(s) sélectionné(s) – {nb_effets} effets secondaires détectés", table, dcc.Graph(figure=piechart, style={"width": "100%"})

# Callback d'export CSV
@dash.callback(
    Output("download-dataframe", "data"),
    Input("btn-export", "n_clicks"),
    State("dropdown-vaccins", "value"),
    prevent_initial_call=True
)
def export_csv(n_clicks, selected_vaccins):
    if not selected_vaccins:
        return dash.no_update

    data = {v: Counter() for v in selected_vaccins}
    for _, row in df[df['vaccine_name'].apply(lambda x: any(v in x for v in selected_vaccins))].iterrows():
        for v in row['vaccine_name']:
            if v in selected_vaccins:
                data[v].update(row['reactions'])

    all_effects = sorted({effet for d in data.values() for effet in d})
    heatmap_data = pd.DataFrame(index=selected_vaccins, columns=all_effects).fillna(0)
    for v in selected_vaccins:
        for effet in data[v]:
            heatmap_data.loc[v, effet] = data[v][effet]

    csv_string = heatmap_data.reset_index().to_csv(index=False, encoding='utf-8')
    return dict(content=csv_string, filename="effets_secondaires_vaccins.csv")
