from flask import Flask, request, Response, jsonify
import boto3
import os
import datetime
import uuid
import json
from boto3.dynamodb.conditions import Key
from flask_sqlalchemy import SQLAlchemy

# App Initialization
app = Flask(__name__)

app.config.from_pyfile('./config/appconfig.cfg')
CONF = f"postgresql://{app.config['PG_USER']}:{app.config['PG_PASSWORD']}@{app.config['PG_HOST']}:{app.config['PG_PORT']}/{app.config ['PG_DATABASE']}"
app.config['SQLALCHEMY_DATABASE_URI'] = CONF

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
db = SQLAlchemy(app)

# Models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['GET'])
def get():
    return ""


@app.route('/ping', methods=['GET'])
def ping():
    return ""

@app.route('/postgres-item', methods=['GET'])
def itemget():
    query = '''CREATE TABLE if not exists item(id serial PRIMARY KEY, title VARCHAR (200) UNIQUE NOT NULL, content VARCHAR (200) NOT NULL);'''
    db.engine.execute(query)

    items = []
    for item in db.session.query(Item).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)

    return jsonify(items)


@app.route('/postgres-item', methods=['POST'])
def itemadd():
    query = '''CREATE TABLE if not exists item(id serial PRIMARY KEY, title VARCHAR (200) UNIQUE NOT NULL, content VARCHAR (200) NOT NULL);'''
    db.engine.execute(query)

    request_data = request.get_json()
    title = request_data["title"]
    content = request_data["content"]

    entry = Item(title, content)
    db.session.add(entry)
    db.session.commit()

    return jsonify("item created")

@app.route('/postgres-item', methods=['PUT'])
def update_item():
    id_to_update = request.args.get('id')

    request_data = request.get_json()
    new_title = request_data["title"]
    new_content = request_data["content"]

    db.session.query(Item).filter_by(id=id_to_update).update(
        dict(title=new_title, content=new_content))
    db.session.commit()
    return "update_item" + id_to_update

@app.route('/postgres-item', methods=['DELETE'])
def delete_item():
    id_to_delete = request.args.get('id')
    db.session.query(Item).filter_by(id=id_to_delete).delete()
    db.session.commit()
    return "item_deleted: " + id_to_delete

def make_response(rv):
    resp = Response(rv)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
