import os
import pandas as pd
from ..db.connection import get_omnisci_connection, get_postgre_connection
from multiprocessing import Process

min_query_size = 40

def create_url(id, url):
    return f"<a href=//{url} >{id}</a>"

def get_museums():
    path = os.path.dirname(os.path.realpath(__file__))
    countries = []
    with open(path + "/../museums.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            countries.append(line.strip())
    return countries

def get_countries():
    countries = pd.read_csv("app/countries.csv")
    country_list = [f"{name}, {code}" for name, code in zip(countries['country'], countries['code'])]
    return country_list

def query_date_ids(ids):
    query = f"""
                SELECT DISTINCT date_original, date_english, date_debug, location_mapped_country,
                    date_start, date_end, date_match_id,
                    date_match_label, date_match_score, date_debug_spatial, date_match_spatial,
                    count(*) AS 'count_obj'
                FROM objects
                WHERE id IN ({ids})
                GROUP BY date_original, date_english, date_debug, date_start, date_end, 
                        location_mapped_country,date_match_id,
                        date_match_label, date_match_score, date_debug_spatial, date_match_spatial
                ORDER BY count_obj DESC
                LIMIT 300
                """
    con = get_omnisci_connection()
    df = pd.read_sql(query, con)
    return df

def query_validated_dates():
    query = f"""
                SELECT DISTINCT date_original, date_english, date_debug, location_mapped_country,
                date_start, date_end, date_match_id,
                date_match_label, date_match_score, date_debug_spatial, date_match_spatial
                FROM tl_date_checked
                """

    con = get_postgre_connection()
    df = pd.read_sql(query, con)
    return df

def query_manual_dates():
    query = f"""
                SELECT DISTINCT input_string, countries
                FROM tl_date_manual_mapping
                """

    con = get_postgre_connection()
    df = pd.read_sql(query, con)
    df['countries'] = df.countries.apply(lambda x: x.split(','))
    df = df.explode('countries')
    return df

def filter_local_dates(df_omni):
    df_local = query_validated_dates()
    df_man = query_manual_dates()

    df = (
        df_omni.merge(df_local,
                      on=['date_original', 'date_english', 'date_debug', 'location_mapped_country',
                          'date_start', 'date_end', 'date_match_id', 'date_match_label', 'date_match_score',
                          'date_debug_spatial', 'date_match_spatial'],
                      how='left',
                      indicator=True)
        .query('_merge == "left_only"')
        .drop(columns='_merge')
        .merge(df_man,
               left_on=['date_english', 'location_mapped_country'],
               right_on=['input_string', 'countries'],
               how='left',
               indicator=True)
        .query('_merge == "left_only"')
        .drop(columns=['_merge', 'input_string', 'countries'])
    )

    return df

def query_dates(input_string, museum, flag, score_start, score_end, query_size=50):

    conditions = ""
    if not flag:
        conditions = conditions + f" AND date_flags = 'FF-CH' "
    else:
        conditions = conditions + f" AND date_flags = '{flag}' "
    if input_string:
        conditions = conditions + f" AND date_debug LIKE '%{input_string}%' "
    if museum is not None and museum != "All museums":
        conditions = conditions + f" AND datasource_id = '{museum}' "
    if score_start:
        conditions = conditions + f" AND date_match_score >= {score_start} "
    if score_end:
        conditions = conditions + f" AND date_match_score <= {score_end} "

    query = f"""
            SELECT DISTINCT date_original, date_english, date_debug, location_mapped_country,
                date_start, date_end, date_match_id, datasource_id,
                date_match_label, date_match_score, date_debug_spatial, date_match_spatial,
                count(*) AS 'count_obj'
            FROM objects
            WHERE location_mapped_country is not null
                    {conditions}
            GROUP BY date_original, date_english, date_debug, date_start, date_end, 
                    location_mapped_country,date_match_id, datasource_id,
                    date_match_label, date_match_score, date_debug_spatial, date_match_spatial
            ORDER BY count_obj DESC
            LIMIT {query_size}
            """

    con = get_omnisci_connection()
    df_omni = pd.read_sql(query, con)

    df = filter_local_dates(df_omni)

    print(f"columns:{df.columns}")

    if len(df) < min_query_size and len(df_omni) == query_size:
        query_size += 50
        df = query_dates(input_string, museum, flag, score_start, score_end, query_size=query_size)

    return df

def date_details(date_english, location_mapped_country, museum):
    condition_museum = ""
    if museum is not None and museum != "All museums":
        condition_museum = f"AND datasource_id = '{museum}'"

    con=get_omnisci_connection()
    query = f"""
        SELECT id, url_object_page, location_debug, attribute_name_english
        FROM objects
            WHERE date_english = '{date_english}'
                AND location_mapped_country = '{location_mapped_country}'
                {condition_museum}
        LIMIT 100
        """
    df = pd.read_sql(query, con)
    return df

def insert_checked_date(df):
    # Set variable to check if location debug in tl_date_checked
    con=get_postgre_connection()
    max_value = pd.read_sql("select count(*) from tl_date_checked", con)
    max_value += 1
    df["id"] = max_value
    df.to_sql(name="tl_date_checked", con=con, if_exists='append', index=False)

#import sqlalchemy
def run_update_statement(statement):
    print(statement)
    con = get_omnisci_connection()
    #con = sqlalchemy.create_engine(con)

    con.execute(statement)
    con.commit()


def update_objects_flag(df):
    df = df.iloc[0]
    if df["correct"] == 0:
        flag = "FF-IN"
    else:
        flag = "NF-CK"

    statement = f""" UPDATE objects 
                    SET date_flags = '{flag}'
                    WHERE date_english = '{df["date_english"]}'
                        AND date_debug = '{df["date_debug"]}' 
                        AND date_match_label = '{df["date_match_label"]}' """
    if df["location_mapped_country"] is not None:
        statement += f""" AND location_mapped_country = '{df["location_mapped_country"]}' """

    p = Process(target=run_update_statement, args=(statement,))
    p.start()
    p.join()

