import plotly.express as px
import pandas as pd
import numpy as np
from .data_loader import load_country_counts

def sexe_distribution_graph(df):
    df_gender = df['sex'].value_counts().reset_index()
    df_gender.columns = ['Sexe', 'Nombre de cas']

    fig = px.bar(
        df_gender,
        x='Sexe', y='Nombre de cas', color='Sexe', text='Nombre de cas',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4'],
        height=450,
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        title=None,
        plot_bgcolor='#1e1e2f', 
        paper_bgcolor='#1e1e2f'
    )
    return fig

def age_distribution_graph(df):
    bins = [0, 18, 35, 50, 65, 80, 100]
    labels = ['0-18', '19-35', '36-50', '51-65', '66-80', '81-100']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    df_age = df['age_group'].value_counts().sort_index().reset_index()
    df_age.columns = ['Tranche d\'âge', 'Nombre de cas']

    fig = px.bar(
        df_age,
        x='Tranche d\'âge', y='Nombre de cas', color='Tranche d\'âge', text='Nombre de cas',
        height=450,
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        title=None,
        plot_bgcolor='#1e1e2f', paper_bgcolor='#1e1e2f'
    )
    return fig

def top_effects_graph(df):
    df_effects = df.explode('reactions')
    top_effects = df_effects['reactions'].value_counts().nlargest(10).reset_index()
    top_effects.columns = ['Reaction', 'Nombre de cas']

    fig = px.bar(
        top_effects,
        x='Reaction', y='Nombre de cas', color='Reaction',
        height=450,
    )
    fig.update_layout(xaxis_tickangle=-45, plot_bgcolor='#1e1e2f', paper_bgcolor='#1e1e2f')
    return fig

def top_products_graph(df):
    df_products = df.explode('product_names')
    top_products = df_products['product_names'].value_counts().nlargest(10).reset_index()
    top_products.columns = ['Produit', 'Nombre de cas']

    rename_dict = {
        'TETANUS (TETANUS VACCINE)': 'Tetanus',
        'INFLUENZA A (H1N1) 2009 MONOVALENT VACCINE': 'H1N1 (2009)',
        'HUMAN PAPILLOMA VACCINE': 'HPV',
        'FLU VACCINE': 'Flu',
        'INFLUENZA VACCINE': 'Influenza',
        'PNEUMOCOCCAL VACCINE': 'Pneumococcal'
    }
    top_products['Produit court'] = top_products['Produit'].replace(rename_dict)

    fig = px.bar(
        top_products,
        x='Produit court', y='Nombre de cas', color='Produit court',
        height=450, 
    )
    fig.update_layout(
        xaxis_tickangle=-30,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        showlegend=True,
        xaxis={'showticklabels': False, 'title': None},
        plot_bgcolor='#1e1e2f', paper_bgcolor='#1e1e2f'
    )
    return fig

def plot_world_map():
    country_counts = load_country_counts()
    country_counts['log_count'] = np.log1p(country_counts['count'])

    fig = px.choropleth(
        country_counts,
        locations="country",
        locationmode="ISO-3",
        color="log_count",
        color_continuous_scale="Blues",
        title="Nombre de déclarations d'effets secondaires par pays",
        labels={"log_count": "Log(Nombre de cas)"}
    )

    fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    paper_bgcolor="#1e1e2f",
    plot_bgcolor="#1e1e2f",
    font=dict(color="white"),
    title_x=0.5,
    height=450
    )


    return fig