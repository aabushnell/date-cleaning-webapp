import pandas as pd
import numpy as np
from sqlalchemy import inspect
from ..db.connection import get_postgre_connection

def get_tables():
    # Get relevant tables that start with tl_loc
    tables = []
    tables.append("tl_date_checked")
    tables.append("tl_date_manual_mapping")
    tables.append("tl_chrono_cache")
    #tables.append("tl_idai")
    tables.append("tl_synonyms")
    #tables = [tl for tl in inspect(con).get_table_names() if "tl_date" in tl]
    # Return tables sorted by reverse length of name for manual to be first
    return sorted(tables, key=len, reverse=True)


def table_value(tl_name):
    # Set query for table and retrieve all as dataframe
    query = f"""
            SELECT *
            FROM {tl_name}
            """
    con=get_postgre_connection()

    table_df = pd.read_sql(query, con)
    # Return entire table
    return table_df


def submit_edits(tl_name, tl_dict):
    # Make table_dict into df
    con = get_postgre_connection()
    update_table = pd.DataFrame.from_dict(tl_dict)
    update_table = update_table.replace(r'^\s*$', np.nan, regex=True)
    # If table is manual mapping make coordinates and ids as ints and floats

    # Replace table
    try:
        update_table.dropna(subset=["column2"], inplace=True)
        update_table.to_sql(name=tl_name, con=con, if_exists='append', index=False, chunksize=500)
        return True
    except:
        return False
