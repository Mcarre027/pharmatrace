import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
from collections import Counter

# Charger les données nettoyées
df = pd.read_csv('data/df_clean.csv')

# Initialiser l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Définir les pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div([
        html.H1("Tableau de bord - Effets secondaires des vaccins", style={'textAlign': 'center'}),

        html.Div([
            html.A("Heatmap interactive", href="/", style={"margin-right": "20px"}),
            html.A("Exploration complète", href="/exploration-complete")
        ], style={'textAlign': 'center', 'margin': '20px'}),

        html.Div(id='page-content')
    ])
])

# Page 1 : Heatmap interactive
heatmap_layout = html.Div([
    html.H2("Heatmap interactive : Vaccins vs Effets secondaires", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Choisir un vaccin :"),
        dcc.Dropdown(
            id='vaccine-dropdown',
            options=[{'label': v, 'value': v} for v in sorted(df['vaccine_name'].explode().dropna().unique())],
            value=None,
            multi=True,
            placeholder="Sélectionner un ou plusieurs vaccins"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='heatmap'),
])

# Callback de la heatmap interactive
@app.callback(
    Output('heatmap', 'figure'),
    Input('vaccine-dropdown', 'value')
)
def update_heatmap(selected_vaccines):
    filtered_df = df.copy()
    if selected_vaccines:
        filtered_df = filtered_df[filtered_df['vaccine_name'].apply(lambda x: any(v in x for v in selected_vaccines))]
    exploded = filtered_df.explode('vaccine_name').explode('reactions')
    heatmap_data = exploded.groupby(['vaccine_name', 'reactions']).size().unstack(fill_value=0)
    fig = px.imshow(heatmap_data, text_auto=True, aspect='auto',
                    labels={'x': 'Effets secondaires', 'y': 'Vaccin', 'color': 'Fréquence'},
                    title="Heatmap : Vaccins vs Effets secondaires")
    return fig

# Page 2 : Exploration complète
exploration_layout = html.Div([
    html.H2("Exploration Complète des Données", style={'textAlign': 'center'}),

    html.H4("1. Répartition par sexe"),
    dcc.Graph(
        figure=px.bar(
            df['sex'].value_counts().reset_index().rename(columns={'index': 'sex', 'sex': 'count'}),
            x='sex', y='count',
            labels={'sex': 'Sexe', 'count': 'Nombre de déclarations'},
            title="Répartition par sexe"
        )
    ),
    html.P("""Ce graphique montre une répartition déséquilibrée des effets secondaires rapportés selon le sexe. 
On observe que près de deux tiers des déclarations concernent des femmes..."""),

    html.H4("2. Top 10 effets secondaires"),
    dcc.Graph(
        figure=px.bar(
            pd.DataFrame(Counter(sum(df['reactions'], [])).most_common(10), columns=["Reaction", "Count"]),
            x='Reaction', y='Count', title="Top 10 effets secondaires"
        )
    ),
    html.P("""Ce graphique présente les 10 effets secondaires les plus fréquemment déclarés suite à l’administration d’un vaccin..."""),

    html.H4("3. Pays les plus rapporteurs"),
    dcc.Graph(
        figure=px.bar(
            df['country'].value_counts().head(10).reset_index().rename(columns={'index': 'country', 'country': 'count'}),
            x='country', y='count',
            labels={'country': 'Pays', 'count': 'Nombre de déclarations'},
            title="Pays les plus rapporteurs"
        )
    ),
    html.P("""Le graphique met en évidence une forte disparité entre les pays..."""),

    html.H4("4. Déclarations par mois"),
    dcc.Graph(
        figure=px.line(
            df.assign(month=pd.to_datetime(df['date']).dt.to_period('M'))
              .groupby('month').size().reset_index(name='count'),
            x='month', y='count', title="Déclarations par mois"
        )
    ),
    html.P("""Ce graphique montre l’évolution mensuelle du nombre de déclarations..."""),

    html.H4("5. Vaccins les plus déclarés"),
    dcc.Graph(
        figure=px.bar(
            pd.DataFrame(Counter(sum(df['vaccine_name'], [])).most_common(10), columns=["Vaccine", "Count"]),
            x='Vaccine', y='Count', title="Top 10 vaccins ou médicaments associés"
        )
    ),
    html.P("""Ce graphique présente les 10 produits médicaux les plus fréquemment associés à des effets secondaires..."""),

    html.H4("6. Répartition par tranche d’âge"),
    dcc.Graph(
        figure=px.bar(
            df.assign(age_group=pd.cut(df['age'], bins=[0,18,35,50,65,80,100],
                                       labels=['0-18','19-35','36-50','51-65','66-80','81-100']))
              .groupby('age_group').size().reset_index(name='count'),
            x='age_group', y='count', title="Répartition par tranche d’âge"
        )
    ),
    html.P("""Ce graphique montre la répartition des déclarations d’effets secondaires selon les tranches d’âge..."""),

    html.H4("7. Heatmap complète"),
    dcc.Graph(
        figure=px.imshow(
            df.explode('vaccine_name').explode('reactions')
              .groupby(['vaccine_name', 'reactions']).size().unstack(fill_value=0),
            text_auto=True, aspect='auto',
            labels={'x': 'Effets secondaires', 'y': 'Vaccin', 'color': 'Fréquence'},
            title="Heatmap : Vaccins vs Effets secondaires (complète)"
        )
    ),
    html.P("""Cette heatmap croise les effets secondaires les plus fréquents avec les vaccins les plus déclarés...""")
])

# Routing
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/exploration-complete':
        return exploration_layout
    return heatmap_layout

# Lancement
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port)
