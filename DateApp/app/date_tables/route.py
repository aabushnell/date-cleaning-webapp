from flask import Blueprint, render_template, jsonify, request, make_response
from .models import *

date_tables = Blueprint('tables', __name__, template_folder='../templates', static_folder='../static')


@date_tables.route("/")
def show():
    date_tables = get_tables()
    init_table = table_value("tl_date_manual_mapping") # Always display manual locations first
    #date_tables.remove("tl_date_manual_mapping")
    #date_tables = ["tl_date_manual_mapping"] + date_tables

    return render_template("tables.html", date_tables=date_tables, init_table=init_table,
                            column_names=list(init_table.columns), row_data=init_table.to_dict('records'))


@date_tables.route("/tables/", methods=["GET", "POST"])
def show_table():
    tl_ = request.get_json()
    display_table = table_value(tl_)
    return jsonify(row_data=display_table.to_dict('records'), column_names=list(display_table.columns))


@date_tables.route("/submit_changes/", methods=["GET", "POST"])
def submit_changes():
    table_ = request.get_json()
    print(type(table_))
    print(table_)
    submit_edits(table_[0], table_[1])
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res
