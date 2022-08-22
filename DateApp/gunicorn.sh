#!/bin/sh
gunicorn --env SCRIPT_NAME=/dateapp --bind 0.0.0.0:8083 "run:create_app(config_filename=\"../config.py\")"
