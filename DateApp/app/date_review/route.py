from flask import Blueprint, render_template, jsonify, request, make_response
from .models import *

date_review = Blueprint('date_review', __name__, template_folder='../templates', static_folder='../static')
lines_to_update = {"line_number": [], "correct": []}

df = None
@date_review.route("/query/", methods=["POST"])
def query():

    if len(request.files) > 0:
        objects_df = pd.read_csv(request.files.get('file'))
        id_list = ""
        for id_ in objects_df.id.to_list():
            id_list = f"{id_list},'{id_}'"

        dataframe = query_date_ids(id_list[1:len(id_list)])
    else:
        input_string = None
        museum = None
        flag = None
        score_start = None
        score_end = None
        if len(request.json) > 0:
            if 'search_input_string' in request.json:
                input_string = request.json.get("search_input_string")
            if 'museums' in request.json:
                museum = request.json.get("museums")
            if 'flag' in request.json:
                flag = request.json.get("flag")
            if 'score_start' in request.json:
                score_start = request.json.get("score_start")
            if 'score_end' in request.json:
                score_end = request.json.get("score_end")

        query_size = 50
        dataframe = query_dates(input_string, museum, flag, score_start, score_end, query_size=query_size)


        id = range(0, len(dataframe))
        dataframe["id"] = id
        global df
        df = dataframe

    return jsonify(data=dataframe.to_dict('records'))

@date_review.route("/", methods=["GET", "POST"])
def show():
    flags = ["FF-CH", "NF-CK", "FF-IN"]#, "FF-NULL", "NF-NU"]
    return render_template("review.html", museum_ids=get_museums(),flags=flags,
                           country_list=get_countries())


@date_review.route("/more_info/", methods=["GET", "POST"])
def more_info():
    json = request.get_json()
    global df
    df_to_query = df.iloc[json.get("line_number")]

    df_result = date_details(df_to_query["date_english"], df_to_query["location_mapped_country"], json.get("museum"))
    df_result["id"] = df_result[['id', 'url_object_page']].apply(lambda x: create_url(x[0],x[1]), axis=1)
    df_result.drop('url_object_page', inplace=True, axis=1)
    return jsonify(row_data=df_result.to_dict('records'), column_names=list(df_result.columns),
                   date_debug=df_to_query["date_debug"], location_mapped_country=df_to_query["location_mapped_country"],
                   date_match_label=df_to_query["date_match_label"], date_match_spatial=df_to_query["date_match_spatial"],
                   date_start=int(df_to_query["date_start"]), date_end=int(df_to_query["date_end"]))


@date_review.route("/get_row_date/", methods=["GET", "POST"])
def get_row_date():
    json = request.get_json()
    global df
    df_to_query = df.iloc[json.get("line_number")]
    return jsonify(date_english=df_to_query["date_debug"])


@date_review.route("/save/", methods=["POST"])
def save_checked_date():
    json = request.get_json()
    df_to_update = df.iloc[json.get("line_number")]

    df_ = pd.DataFrame({"id": 0,
                        "date_original": df_to_update["date_original"],
                        "date_english": df_to_update["date_english"],
                        "date_start": df_to_update["date_start"],
                        "date_end": df_to_update["date_end"],
                        "date_debug": df_to_update["date_debug"],
                        "date_debug_spatial": df_to_update["date_debug_spatial"],
                        "date_match_label": df_to_update["date_match_label"],
                        "date_match_score": df_to_update["date_match_score"],
                        "date_match_spatial": df_to_update["date_match_spatial"],
                        "date_match_id": df_to_update["date_match_id"],
                        "correct": json.get("correct"),
                        "location_mapped_country": df_to_update["location_mapped_country"],
                        "collection_id": df_to_update["datasource_id"]}, index=["id"])
    #df_to_update["correct"] = json.get("correct")
    #df_to_update = df_to_update.drop('id')
    #df_to_update = df_to_update.drop('count_obj')

    insert_checked_date(df_)
    lines_to_update["line_number"].append(json.get("line_number"))
    lines_to_update["correct"].append(json.get("correct"))
    #update_objects_flag(df_)
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res


