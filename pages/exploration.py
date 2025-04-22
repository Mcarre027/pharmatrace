from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from utils.data_loader import load_data
from utils.graphs import (
    sexe_distribution_graph,
    age_distribution_graph,
    top_effects_graph,
    top_products_graph
)

dash.register_page(__name__, path="/exploration", name="Exploration")

# Chargement des données
df = load_data()

layout = dbc.Container([
    html.H2("Exploration des données sur les effets secondaires", className="my-5 text-center"),

    dbc.Row([
        dbc.Col([
            html.H4("Répartition par genre", className="mb-3 text-center"),
            dcc.Graph(figure=sexe_distribution_graph(df), id="graph-sexe", className="centered-plot"),
            html.P("""
               Ce graphique montre une répartition déséquilibrée des effets secondaires rapportés selon le sexe.
                On observe que près de deux tiers des déclarations concernent des femmes.
                Cette surreprésentation peut s’expliquer par plusieurs facteurs : une réactivité plus élevée des femmes au système de pharmacovigilance, des habitudes de consultation médicale différentes, ou encore une sensibilité biologique potentiellement accrue à certains principes actifs.
            """, className="text-justify")
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("Distribution par âge", className="mb-3 text-center"),
            dcc.Graph(figure=age_distribution_graph(df), id="graph-age", className="centered-plot"),
            html.P("""
                Cette visualisation permet de comprendre quelles tranches d’âge sont les plus concernées par les effets secondaires rapportés.
                On observe que les personnes âgées de 66 à 80 ans sont les plus touchées, avec 206 cas rapportés, suivies par la tranche 51–65 ans avec 168 cas.
                Ces deux groupes regroupent à eux seuls la majorité des signalements, ce qui pourrait s’expliquer par une plus grande consommation de médicaments dans ces tranches d’âge, en lien avec des pathologies chroniques ou des traitements au long cours.
                Les tranches plus jeunes, comme 0–18 ans et 19–35 ans, présentent un nombre de cas nettement inférieur (38 et 67 cas respectivement), ce qui peut refléter une exposition médicamenteuse plus faible, une meilleure tolérance, ou encore une sous-déclaration des effets secondaires dans ces populations.
                Ce type de visualisation est essentiel pour orienter les efforts de pharmacovigilance et adapter les messages de prévention selon les groupes d’âge les plus exposés.


            """, className="text-justify")
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("Top 10 effets secondaires", className="mb-3 text-center"),
            dcc.Graph(figure=top_effects_graph(df), id="graph-effets", className="centered-plot"),
            html.P("""
                Ce graphique présente les 10 effets secondaires les plus fréquemment déclarés dans notre échantillon de données issues de pharmacovigilance.
                En tête, on retrouve la fièvre (Pyrexia), avec plus de 70 cas rapportés, suivie de la douleur (Pain) et de la dyspnée (essoufflement), avec respectivement 62 et 57 signalements. Ces réactions figurent parmi les plus courantes dans les déclarations d’effets secondaires, quel que soit le type de médicament concerné.
                Des symptômes tels que le malaise, la fatigue, la nausée et les maux de tête apparaissent également de manière significative, avec des fréquences proches (autour de 50 cas).
                En revanche, des réactions comme l’éruption cutanée (Rash) ou les syndromes pseudo-grippaux (Influenza) sont moins souvent rapportés dans cet échantillon.
                Cette distribution permet de cibler les effets les plus courants à travers les différentes classes médicamenteuses, afin d’améliorer l’information aux patients et la vigilance des professionnels de santé.
            """, className="text-justify")
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("Top 10 des médicaments associés à des effets secondaires", className="mb-3 text-center"),
            dcc.Graph(figure= top_products_graph(df), id="graph-produits", className="centered-plot"),
            html.P("""
                Ce graphique présente les 10 médicaments les plus fréquemment associés à des effets secondaires dans le jeu de données.
                Le médicament XOLAIR se démarque très nettement avec près de 250 cas rapportés, ce qui en fait le produit le plus fréquemment lié à des effets secondaires dans cet échantillon.
                Viennent ensuite Influenza et HUMIRA, avec respectivement environ 130 et 105 signalements, indiquant également une vigilance accrue autour de ces traitements.
                D’autres produits comme DEXAMETHASONE, ASPIRIN ou REVLIMID affichent des volumes de déclarations plus modérés, oscillant entre 70 et 60 cas.
                Enfin, PREDNISONE, SOLIRIS, ENBREL et OMEPRAZOLE clôturent ce classement avec un peu moins de 50 déclarations chacun.
                Il est essentiel de noter que ce type de visualisation ne permet pas à elle seule de conclure à une plus grande dangerosité de certains médicaments.
                Le volume de prescriptions, le profil des patients (âge, comorbidités), ou encore le niveau de surveillance peuvent fortement influencer le nombre de signalements.
                Ce graphique constitue néanmoins un outil d’orientation précieux pour identifier les molécules nécessitant une analyse plus approfondie en pharmacovigilance.
            """, className="text-justify")
        ])
    ])
], fluid=True)
