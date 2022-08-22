from flask import Flask
import datetime


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    #from .user.models import db, login
    #db.init_app(app)

    #login.init_app(app)
    from .date_home.route import date_home
    from .date_check.route import date_check
    from .date_manual.route import date_manual
    from .date_review.route import date_review
    #from .location_filter.route import location_filter
    from .date_tables.route import date_tables
    #from .location_viz.route import location_viz
    #from .user.route import auth
    #from .user.home import home

    app.register_blueprint(date_home, url_prefix="/")
    app.register_blueprint(date_check, url_prefix="/check")
    app.register_blueprint(date_manual, url_prefix="/manual")
    app.register_blueprint(date_review, url_prefix="/review")
    #app.register_blueprint(location_filter, url_prefix="/filter")
    app.register_blueprint(date_tables, url_prefix="/tables")
    #app.register_blueprint(location_viz, url_prefix="/viz")

    @app.context_processor
    def current_year():
        return {'year': datetime.date.today().year}

    return app
