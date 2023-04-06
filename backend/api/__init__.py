from flask import Flask
from api.lib.orm import find_all, build_from_record, find, build_from_records
from api.lib.db import get_db
import api.models as models

import json
import psycopg2

def create_app(db_name):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = db_name)

    @app.route("/")
    def root_url():
        return "welcome to the adventureworks app"

    @app.route("/persons")
    def person_index():
        conn=get_db()
        cursor=conn.cursor()
        person_objs=find_all(cursor, models.Person)
        person_dict=[person_obj.__dict__ for person_obj in person_objs]
        return person_dict

    @app.route("/persons/lastname/<lastname>")
    def person_lastname_show(lastname):
        conn=get_db()
        cursor=conn.cursor()
        statement='''
        SELECT * 
        FROM person.person
        WHERE lastname=%s;
        '''
        cursor.execute(statement, (lastname,))
        person_records=cursor.fetchall()
        person_objs=build_from_records(models.Person, person_records)
        person_dicts=[person_obj.__dict__ for person_obj in person_objs]
        return person_dicts

    @app.route("/addresses")
    def address_index():
        conn=get_db()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM person.address;")     
        address_records=cursor.fetchall()
        address_objs=build_from_records(models.Address, address_records)
        address_dicts=[address_obj.__dict__ for address_obj in address_objs]
        return address_dicts

    @app.route("/person/addresses/<person_businessentityid>")
    def address_id(person_businessentityid):
        conn=get_db()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM person.person WHERE businessentityid=%s;", (person_businessentityid,))
        person_record=cursor.fetchone()
        person_obj=build_from_record(models.Person, person_record)
        add_relation=person_obj.to_json(conn)
        return add_relation



    return app
