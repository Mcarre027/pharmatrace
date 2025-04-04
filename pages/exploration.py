from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from utils.data_loader import load_data
from utils.graphs import (
    sexe_distribution_graph,
    age_distribution_graph,
    top_effects_graph,
    top_vaccines_graph
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
                Cette surreprésentation peut s'expliquer par plusieurs facteurs tels qu'une réactivité plus élevée des femmes au système de pharmacovigilance 
                ou une différence biologique potentielle dans la réponse immunitaire aux vaccins.
            """, className="text-justify")
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("Distribution par âge", className="mb-3 text-center"),
            dcc.Graph(figure=age_distribution_graph(df), id="graph-age", className="centered-plot"),
            html.P("""
                Cette visualisation permet de comprendre quelles tranches d'âge sont les plus concernées par les effets secondaires rapportés.
                On observe que les personnes âgées de 66 à 80 ans sont les plus touchées, avec 206 cas rapportés, suivies par la tranche 51-65 ans avec 168 cas. 
                Ces deux tranches regroupent à elles seules la majorité des signalements, ce qui pourrait s’expliquer par une plus grande exposition vaccinale dans ces groupes prioritaires, 
                notamment au début des campagnes de vaccination.
                Les tranches plus jeunes, comme 0-18 ans et 19-35 ans, présentent un nombre de cas nettement inférieur (38 et 67 cas respectivement), ce qui peut refléter à la fois une moindre couverture vaccinale initiale, 
                une meilleure tolérance aux vaccins ou encore une sous-déclaration des effets secondaires dans ces populations.
                Ce type de visualisation est essentiel pour orienter les efforts de pharmacovigilance et adapter la communication sur la sécurité vaccinale selon les groupes d’âge.
            """, className="text-justify")
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("Top 10 effets secondaires", className="mb-3 text-center"),
            dcc.Graph(figure=top_effects_graph(df), id="graph-effets", className="centered-plot"),
            html.P("""
                Ce graphique présente les 10 effets secondaires les plus fréquemment déclarés suite à l'administration d'un vaccin dans notre échantillon de données.
                En tête, on retrouve la fièvre (Pyrexia), avec plus de 70 cas rapportés, suivie de la douleur (Pain) et la dyspnée (essoufflement), avec respectivement 62 et 57 signalements. 
                Ces réactions sont typiquement associées à la réponse immunitaire post-vaccinale.
                Les effets secondaires comme le malaise, la fatigue, la nausée et les maux de tête apparaissent également de manière significative, avec des fréquences proches les unes des autres (autour de 50 cas). 
                En revanche, des symptômes comme l’éruption cutanée (Rash) ou des syndromes pseudo-grippaux (Influenza) sont moins souvent rapportés dans cette population.
                Cette distribution permet de cibler les effets les plus courants pour mieux informer les patients en amont de la vaccination, et alerter les professionnels de santé sur les signaux potentiels à surveiller.
            """, className="text-justify")
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("Top 10 vaccins rapportés", className="mb-3 text-center"),
            dcc.Graph(figure=top_vaccines_graph(df), id="graph-vaccins", className="centered-plot"),
            html.P("""
                Ce graphique présente les 10 vaccins les plus fréquemment associés à des effets secondaires dans le jeu de données.
                Le vaccin XOLAIR se démarque très nettement avec près de 250 cas rapportés, ce qui en fait le vaccin le plus fréquemment lié à des effets secondaires dans cet échantillon. 
                Viennent ensuite Influenza et HUMIRA, avec respectivement environ 130 et 105 signalements, indiquant également une vigilance accrue autour de ces produits.
                Les autres vaccins comme DEXAMETHASONE, ASPIRIN ou encore REVLIMID affichent des volumes de déclarations plus modérés, oscillant entre 70 et 60 cas. 
                Enfin, les vaccins PREDNISONE, SOLIRIS, ENBREL et OMEPRAZOLE clôturent ce classement avec un peu moins de 50 déclarations chacun.
                Il est essentiel de noter que ce type de visualisation ne permet pas à elle seule de conclure à une plus grande dangerosité de certains vaccins : 
                le volume de prescriptions, les caractéristiques des patients (âge, comorbidités) ou encore le niveau de surveillance peuvent fortement influencer le nombre de signalements.
                Ce graphique constitue toutefois un outil d’orientation utile pour cibler les produits nécessitant une analyse plus approfondie en pharmacovigilance.
            """, className="text-justify")
        ])
    ])
], fluid=True)
