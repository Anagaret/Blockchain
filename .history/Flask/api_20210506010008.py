import flask
from flask import redirect, url_for, request, jsonify
import sqlite3
import json
from werkzeug.utils import secure_filename
from classes.pictureblock import PictureBlock

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/user/<int:user_id>/artwork", methods=["POST"])
def add_artwork(user_id):
    connect = sqlite3.connect("./database.db")
    f = request.files["picture"]
    if "image" not in f.mimetype:
        return {"error": "Le fichier transmit n'est pas une image ."}
    price = request.form.get("price", None)
    if price is None:
        return {"error": "Le prix n'est pas present ."}
    try:
        price = float(price.replace(",", "."))
        f.save("./pictures/" + secure_filename(f.filename))
        try:
            sql_create_artwork = """ INSERT INTO artwork(price, filename)
                                VALUES (:price, :filename) """
            data = json.loads(json.dumps({"price": price, "filename": f.filename}))
            cursor = connect.cursor()
            cursor.execute(sql_create_artwork, data)
            id_artwork = cursor.lastrowid
            connect.commit()
            block = PictureBlock(f.filename)
            sql_create_block = """ INSERT INTO block("index", previous_hash, "timestamp", hash, nonce, id_artwork, id_user_creator, id_user_owner, data) 
                                VALUES (:index, :previous_hash, :timestamp, :hash, :nonce, :id_artwork, :id_user_creator, :id_user_owner, :data) """

            data_block = {
                "index": block.index,
                "previous_hash": block.previous_hash,
                "timestamp": block.timestamp,
                "hash": block.hash,
                "nonce": block.nonce,
                "id_artwork": id_artwork,
                "id_user_creator": user_id,
                "id_user_owner": user_id,
                "data": "block.data",
            }
            json.loads(json.dumps(data_block))
            cursor.execute(sql_create_block, json.loads(json.dumps(data_block)))
            connect.commit()
            return {
                "id": id_artwork,
                "price": price,
                "filename": f.filename,
                "available": 1,
                "id_user_creator": user_id,
                "id_user_owner": user_id,
            }

        except sqlite3.Error as er:
            return {"error": "Probleme insertion artwork"}
    except sqlite3.Error as er:
        return {"error": "Le prix n'est pas au bon format ."}


@app.route("/artwork/<int:id_artwork>/", methods=["GET"])
def get_artwork(id_artwork):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        artwork = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork WHERE b.id_artwork=?""",
            [id_artwork],
        ).fetchone()
        if not artwork:
            artwork = {}
        return jsonify(artwork)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/artwork", methods=["GET"])
def get__all_artwork():
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        artworks = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork """
        ).fetchall()
        if not artworks:
            artworks = {}
        return jsonify(artworks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}
        


@app.route("/user/<int:id_user_creator>/artwork", methods=["GET"])
def get__all_artwork_by_creator(id_user_creator):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        artworks = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork 
         WHERE b.id_user_creator = ? """, [id_user_creator]
        ).fetchall()
        if not artworks:
            artworks = {}
        return jsonify(artworks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}

@app.route("/buy_artwork/<int:id_artwork>", methods=["PUT"])
def buy_artwork(id_artwork):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory

    id_user = request.form.get("id_user", None)
    if id_user is None:
        return {"error": "L'identifiant utilisateur pour l'achat est manquant."}

    try:
        cursor = connect.cursor()
        cursor.executeAll(
            """ UPDATE artwork SET available = 0 WHERE id = ?;
                UPDATE block SET id_user_owner = ? WHERE id_artwork = ?;""",
                [id_artwork,id_user,id_artwork]
        )
        connect.commit()

        
        return { }
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}



app.run()
