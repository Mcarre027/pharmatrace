import dash
from dash import dcc, html, Input, Output, State, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from collections import Counter

# Enregistrement de la page
dash.register_page(__name__, path="/heatmap", name="Heatmap")

# Chargement des données
df = load_data()
produits_uniques = sorted({p for liste in df['product_names'] for p in liste})

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(style={"height": "40px"}),
            html.H2("Heatmap des effets secondaires par médicament", className="mb-4 text-center"),
            html.P("Sélectionnez un ou plusieurs médicaments pour afficher la fréquence des effets secondaires associés."),
            dcc.Dropdown(
                options=[{"label": p, "value": p} for p in produits_uniques],
                value=[produits_uniques[0]],
                multi=True,
                id="dropdown-produits",
                style={"width": "100%"}
            ),
            html.Div(id="heatmap-stats", className="text-info my-3 text-center"),
            dcc.Loading(
                dcc.Graph(id="heatmap", className="centered-plot", style={"width": "100%", "height": "450px"}),
                type="default"
            ),
            html.Div(id="info-empty", className="text-muted mt-3 text-center"),
            html.P("""
                Cette heatmap permet de visualiser l’intensité des effets secondaires en fonction des médicaments sélectionnés.
                Plus la couleur est intense, plus l’effet secondaire est fréquemment rapporté pour ce médicament.
                Cela permet d’identifier rapidement les réactions spécifiques à certains produits, ainsi que les tendances globales de pharmacovigilance.
            """, className="mt-4 text-justify"),

            html.Div(style={"height": "30px"}),

            html.H3("Tableau des effets secondaires", className="text-center mt-5 mb-3"),
            html.Div(style={"height": "20px"}),
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

@dash.callback(
    Output("heatmap", "figure"),
    Output("info-empty", "children"),
    Output("heatmap-stats", "children"),
    Output("table-container", "children"),
    Output("barplot-container", "children"),
    Input("dropdown-produits", "value")
)
def update_heatmap(produits_selection):
    if not produits_selection:
        fig = go.Figure(go.Heatmap(z=[[0]], x=["Effets"], y=["Produit"]))
        fig.update_layout(plot_bgcolor="#1e1e2f", paper_bgcolor="#1e1e2f")
        return fig, "Veuillez sélectionner au moins un produit.", "", "", ""

    df_filtered = df[df['product_names'].apply(lambda x: any(p in x for p in produits_selection))]
    data = {p: Counter() for p in produits_selection}
    for _, row in df_filtered.iterrows():
        for p in row['product_names']:
            if p in produits_selection:
                data[p].update(row['reactions'])

    all_effects = sorted({effet for d in data.values() for effet in d})
    heatmap_data = pd.DataFrame(index=produits_selection, columns=all_effects).fillna(0)
    for p in produits_selection:
        for effet in data[p]:
            heatmap_data.loc[p, effet] = data[p][effet]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale="Viridis",
        text=heatmap_data.values,
        texttemplate="%{text}",
        hovertemplate='Produit : %{y}<br>Effet : %{x}<br>Fréquence : %{z}<extra></extra>',
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
    nb_produits = len(produits_selection)

    table_df = heatmap_data.reset_index().rename(columns={"index": "Produit"})
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

    return fig, "", f"{nb_produits} produit(s) sélectionné(s) – {nb_effets} effets secondaires détectés", table, dcc.Graph(figure=piechart, className="centered-plot")

@dash.callback(
    Output("download-dataframe", "data"),
    Input("btn-export", "n_clicks"),
    State("dropdown-produits", "value"),
    prevent_initial_call=True
)
def export_csv(n_clicks, selected_produits):
    if not selected_produits:
        return dash.no_update

    data = {p: Counter() for p in selected_produits}
    for _, row in df[df['product_names'].apply(lambda x: any(p in x for p in selected_produits))].iterrows():
        for p in row['product_names']:
            if p in selected_produits:
                data[p].update(row['reactions'])

    all_effects = sorted({effet for d in data.values() for effet in d})
    heatmap_data = pd.DataFrame(index=selected_produits, columns=all_effects).fillna(0)
    for p in selected_produits:
        for effet in data[p]:
            heatmap_data.loc[p, effet] = data[p][effet]

    csv_string = heatmap_data.reset_index().to_csv(index=False, encoding='utf-8')
    return dict(content=csv_string, filename="effets_secondaires_medicaments.csv")
