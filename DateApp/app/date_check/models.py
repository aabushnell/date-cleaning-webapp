import pandas as pd
from DateCleaning.DateCleaning import clean_fill_df
from ..db.connection import get_omnisci_connection, get_postgre_connection

def date_info(date_str, country):
    # Set dictionary that contains date output variables
    date_result = {
        "date": "N/A",
        "date_start": "N/A",
        "date_end": "N/A",
        "date_english": "N/A",
        "date_original": "N/A",
        "date_original_lang": "N/A",
        "date_flags": "NULL"
    }
    if country:
        result = clean_fill_df(pd.DataFrame({"date_english": [date_str], "co": [country]}),
                               engine=get_postgre_connection(), debug=True)
    else:
        result = clean_fill_df(pd.Series([date_str]), engine=get_postgre_connection(), debug=True)

    # If return a positive result get following variables
    print("result from clean_date" + str(result.iloc[0]))
    if (not result.empty) or (result.iloc[0]["date_start"] != ""
                        and result.iloc[0]["date_end"] != ""):
        date_result["date_english"] = str(result.iloc[0]["date_english"])
        date_result["date_start"] = str(result.iloc[0]["date_start"])
        date_result["date_end"] = str(result.iloc[0]["date_end"])
        date_result["date_english"] = str(result.iloc[0]["date_english"])
        date_result["date_original"] = str(result.iloc[0]["date_original"])
        date_result["date_original_lang"] = str(result.iloc[0]["date_original_lang"])
        date_result["date_flags"] = str(result.iloc[0]["date_flags"])
        # date_result["date_match_spatial"] = str(result.iloc[0]["date_match_spatial"])
        date_result["log"] = str(result.iloc[0]["log"])
    # If no result just get flags
    else:
        date_result["date_flags"] = str(result.iloc[0]["date_flags"])
    # Return variables in dictionary
    return date_result
