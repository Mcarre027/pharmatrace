import pandas as pd
import ast
import pycountry

def convert_to_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None

def load_data():
    df = pd.read_csv("df_clean.csv")
    df['country'] = df['country'].apply(convert_to_iso3)
    df.dropna(subset=['country'], inplace=True)

    # Important pour ton application Dash :
    df['reactions'] = df['reactions'].apply(ast.literal_eval)
    df['vaccine_name'] = df['vaccine_name'].apply(ast.literal_eval)

    return df

# Cette fonction manquait sûrement ou était mal positionnée
def load_country_counts():
    df = load_data()
    country_counts = df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']
    return country_counts
