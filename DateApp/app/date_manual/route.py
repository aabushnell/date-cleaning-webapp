from flask import Blueprint, make_response, render_template, request, jsonify
from .models import append_manual_date, append_synonym, query_periodo_id
import pandas as pd

date_manual = Blueprint('manual', __name__, template_folder='../templates', static_folder='../static')


@date_manual.route("/", methods=["POST", "GET"])
def manual_date():
    countries = pd.read_csv("app/countries.csv")
    country_list = [f"{name}, {code}" for name, code in zip(countries['country'], countries['code'])]
    return render_template("manual.html", country_list=country_list)


@date_manual.route("/manual_date/", methods=["POST"])
def send_manual_date():
    json = request.get_json()
    df = pd.DataFrame({'id': 0,
                       'input_string': str(json['input_string']).lower().strip(),
                       'date_start': str(json['date_start']).lower().strip(),
                       'date_end': str(json['date_end']).lower().strip(),
                       'comment': str(json['comments']).lower(),
                       'countries': str(json['countries']).strip(),
                       'url_source': str(json['notes']).lower(),
                       "periodo_id": str(json['periodo_id']).lower()}, index=['input_string'])
    global periodo_data
    if (len(periodo_data) != 0):
        df["countries"] = periodo_data[0]["country_list"].iloc[0]
        df["periodo_id"] = periodo_data[0]["periodo_id"].iloc[0]
        periodo_data.clear()
    append_manual_date(df)
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res


@date_manual.route("/submit_synonym/", methods=["POST"])
def send_synonym():
    json = request.get_json()
    d = append_synonym(json)
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res

periodo_data = []
@date_manual.route("/query_periodo/", methods=["POST"])
def query_periodo():
    global periodo_data
    json = request.get_json()
    periodo_id = json["periodo_id"]
    periodo_entry = query_periodo_id(periodo_id)
    periodo_entry["comments"] = f"Periodo: {periodo_entry['label'].iloc[0]} - {periodo_entry['country_list'].iloc[0]}"
    periodo_data.append(periodo_entry)
    return jsonify(periodo_entry=periodo_entry.to_dict("records"))
