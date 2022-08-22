from flask import Blueprint, make_response, render_template, request, jsonify
import os

date_home = Blueprint('home', __name__, template_folder='../templates', static_folder='../static')

@date_home.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")
