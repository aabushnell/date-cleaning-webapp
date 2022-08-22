from flask import Blueprint, render_template, request, jsonify
from .models import *
from pkg_resources import get_distribution

date_check = Blueprint('check', __name__, template_folder='../templates', static_folder='../static')

@date_check.route("/", methods=["POST", "GET"])
def check():
    pkg_version = str("v{}".format(get_distribution("DateCleaning").version))
    countries = pd.read_csv("app/countries.csv")
    country_list = [f"{name}, {code}" for name, code in zip(countries['country'], countries['code'])]
    return render_template("check.html", pkg_version=pkg_version, country_list=country_list)

@date_check.route("/search/", methods=["GET", "POST"])
def search_date():
    date_str = request.get_json().get("date")
    country = request.get_json().get("country")
    if country:
        country = country.split(", ")[1]
    date_query = date_info(date_str, country)

    if 'log' in date_query:
        date_query["log"] = date_query["log"].replace("\n", "</br>")

    date_results = {
        "date_results": date_query
    }
    return jsonify(date_results=date_results)
