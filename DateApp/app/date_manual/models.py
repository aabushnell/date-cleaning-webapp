import pandas as pd
from ..db.connection import get_postgre_connection

def append_manual_date(df):
    # Create dataframe to be appended
    # Input values in dataframe
    con = get_postgre_connection()
    max_value = pd.read_sql("select count(*) as count_mm from tl_date_manual_mapping", con)
    new_id = max_value['count_mm'].iloc[0]
    new_id += 1
    df["id"] = new_id
    df.to_sql('tl_date_manual_mapping', con=con, if_exists='append', index=False)

    #Remove from tl_date_checked
    #date = str(json['input_string']).title().strip()
    #engine.execute(f"DELETE FROM tl_date_checked WHERE input_string = '{date}'")

    return df

def append_synonym(json):
    df = pd.DataFrame(columns = ['original_string',
                                 'synonym',
                                 'comment'])

    # Input values in dataframe
    df = df.append({'original_string': str(json['original_string']).lower().strip(),
                    'synonym': str(json['synonym']).lower().strip(),
                    'comment': str(json['comment']).lower().strip(),
                    'is_date_original': json['is_date_original']}, ignore_index=True)

    engine = get_postgre_connection()
    df.to_sql('tl_synonyms', con=engine, if_exists='append', index=False)
    return df

def query_periodo_id(periodo_id):
    con = get_postgre_connection()
    sql = f"""select * from tl_date_periodo 
                where periodo_id = '{periodo_id}'"""
    periodo_entry = pd.read_sql(sql, con)
    return periodo_entry
