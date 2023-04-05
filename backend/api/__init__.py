from flask import Flask
from api.lib.orm import find_all, build_from_record, find
from api.lib.db import get_db

import json
import psycopg2

def create_app(db_name):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = db_name)
    return app
