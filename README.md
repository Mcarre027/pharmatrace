# PharmaTrace – Analyse exploratoire des effets secondaires médicamenteux

PharmaTrace est un tableau de bord interactif de pharmacovigilance, développé en Python avec Dash, permettant d'explorer les effets secondaires rapportés pour des milliers de médicaments à travers le monde.

## 🎯 Objectif du projet

Fournir une vue claire et synthétique des signaux d'effets secondaires associés à l'administration de médicaments, à partir des données issues de la base OpenFDA.  
L’objectif est d’identifier les profils de patients les plus concernés, les effets les plus fréquemment signalés et les substances actives les plus associées à ces réactions.

## 🔍 Fonctionnalités

- **Heatmap** des effets secondaires par médicament
- Exploration des signalements selon :
  - Le **sexe**
  - La **tranche d’âge**
  - Le **médicament ou principe actif**
- **Top 10** des effets secondaires et des médicaments les plus signalés
- Données issues de la pharmacovigilance internationale (OpenFDA)

## 📊 Technologies utilisées

- Python
- Dash / Plotly
- Pandas
- OpenFDA (base FAERS)

## 📁 Structure du projet

├── app.py # Application Dash ├── data/ │ └── pharma_data.csv # Données nettoyées ├── assets/ │ └── style.css # Feuille de style ├── pages/ │ ├── home.py # Page d'accueil │ ├── heatmap.py # Heatmap interactive │ └── exploration.py # Analyses démographiques ├── utils/ │ ├── data_loader.py # Chargement et filtrage des données │ └── graphs.py # Fonctions de visualisation └── README.md



## 📢 Auteur

Projet réalisé par [Ton Nom] dans le cadre de son portfolio Data Analyst.  
Vous pouvez me retrouver sur [LinkedIn](https://www.linkedin.com/in/matthieu-carre-data/) pour en discuter.

