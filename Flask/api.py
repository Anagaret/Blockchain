import flask 
from flask import redirect, url_for, request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True



app.run()