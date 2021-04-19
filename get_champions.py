import pandas as pd


def get_lol_champions_list():
    df = pd.read_csv("lol_classes.csv")
    return df


def create_champion_dictionary_dict(df):
    return dict(df.values.tolist())


def marshall_champion_data():
    df = get_lol_champions_list()
    champ_dict = create_champion_dictionary_dict(df)
    return champ_dict
