import flask 
from flask import redirect, url_for, request, jsonify
import sqlite3
import json
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/user/<int:user_id>/artwork', methods=['POST'])
def add_artwork(user_id):
    connect = sqlite3.connect('./database.db')
    f = request.files['picture']
    if "image" not in f.mimetype:
        return { 'error' : 'Le fichier transmit n`est pas une image .'}
    body = request.get_json()
    print(request.form)
    # f.save('./pictures/' + secure_filename(f.filename))
    # sql_create_artwork = ''' INSERT INTO artwork VALUES(price, filename)
    #                         VALUES (?, ?) ''' 
    # body['filename'] = f.filename
    # data = json.loads(json.dumps(body))

    # cursor.execute(sql_create_artwork, data)
    # connect.commit()

    return {}

    # sql = ''' ................ '''
    # cursor = connect.cursor()


   


app.run()