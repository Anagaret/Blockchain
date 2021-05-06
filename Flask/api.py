import flask
from flask import redirect, url_for, request, jsonify, flash, render_template
import sqlite3
import json
from werkzeug.utils import secure_filename
from classes.pictureblock import PictureBlock
import bcrypt
import os
import jwt
import re

cwd = os.getcwd()


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'


@app.route("/user", methods=["POST"])
def add_user():
    body = request.get_json()
    connect = sqlite3.connect('./database.db')
    if "email" not in body:
        return {"error": "L'email utilisateur manquant."}

    if "password" not in body:
        return {"error": "Le mot de passe est manquant."}

    if "tel" not in body:
        return {"error": "Le telephone utilisateur est  manquant."}

    if "nom" not in body:
        return {"error": "Le nom est manquant."}
    
    if "prenom" not in body:
        return {"error": "Le prenom est manquant."}

    if "paypal" not in body:
        return {"error": "Le paypal est manquant."}

    if "pseudo" not in body:
        return {"error": "Le pseudo est manquant."}

    if not re.search(r"\S+[@]\w+[.]+\w+",body['email']):
        return {"error": "L'email n'est pas au bon format"}

    if not re.search(r"^[0][6-7]{1}[0-9]{8}$", body['tel']):
        return {"error": "Le numéro n'est pas au bon format. Il doit etre un 06 ou 07."}


    password = hash_password(body["password"])
 
    try:
        sql_create_user = """INSERT INTO user(pseudo, email, tel, nom, prenom, paypal, password)
                   VALUES(:pseudo, :email, :tel, :nom, :prenom, :paypal, :password) """
        data = json.loads(
            json.dumps(
                {
                    "pseudo": body['pseudo'],
                    "email": body['email'],
                    "tel": body['tel'],
                    "nom": body['nom'],
                    "prenom": body['prenom'],
                    "paypal": body['paypal'],
                    "password": password
                }
            )
        )
        cursor = connect.cursor()
        cursor.execute(sql_create_user, data)
        connect.commit()
        id_user = cursor.lastrowid


        return {    "id": id_user,
                    "pseudo": body['pseudo'],
                    "email": body['email'],
                    "tel": body['tel'],
                    "nom": body['nom'],
                    "prenom": body['prenom'],
                    "paypal": body['paypal'],
                }

    except sqlite3.Error as er:
        return {"error": "Doublon d'information"}


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    connect = sqlite3.connect("./database.db")
    try:
        sql = """DELETE FROM user WHERE id = ? """
        cursor = connect.cursor()
        cursor.execute(sql, [user_id])
        connect.commit()
        return {"success": "Utilisateur supprime"}
    except sqlite3.Error as er:
        return {"error": "ID Inexistant, veuillez vous reconnecter"}


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
        f.save(cwd + "/Flask/pictures/" + secure_filename(f.filename))
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
                "data": str(block.data),
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
def get_all_artwork():
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        artworks = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork """
        ).fetchall()
        if not artworks:
            artworks = []
        return jsonify(artworks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/user/<int:id_user_creator>/artwork", methods=["GET"])
def get_all_artwork_by_creator(id_user_creator):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        artworks = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork 
         WHERE b.id_user_creator = ? """,
            [id_user_creator],
        ).fetchall()
        if not artworks:
            artworks = []
        return jsonify(artworks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/buy_artwork/<int:id_artwork>", methods=["PUT"])
def buy_artwork(id_artwork):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory

    body = request.get_json()
    if "id_user" not in body:
        return {"error": "L'identifiant utilisateur pour l'achat est manquant."}

    try:
        cursor = connect.cursor()
        cursor.execute(
            """ UPDATE artwork SET available = 0 WHERE id = ?""", [id_artwork]
        )
        cursor.execute(
            """ 
                UPDATE block SET id_user_owner = ? WHERE id_artwork = ?""",
            [body["id_user"], id_artwork],
        )
        connect.commit()

        return redirect("/artwork/" + str(id_artwork))
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


@app.route("/login", methods=["POST"])
def login():
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory

    body = request.get_json()
    if "email" not in body:
        flash("Please enter")
        # return {"error": "L'email utilisateur manquant."}

    if "password" not in body:
        return {"error": "Le mot de passe est manquant."}

    try:
        cursor = connect.cursor()
        user = cursor.execute(
            """ select * from user where email = ? """, [body["email"]]
        ).fetchone()
        if not user:
            return {"error": "Email non trouvé"}
        if not bcrypt.checkpw(body['password'].encode("utf-8"), user["password"].encode("utf-8")):
            return {"error": "Mot de passe incorrect"}

        token = jwt.encode({'id': user["id"], "pseudo" : user["pseudo"]}, "123456789", algorithm="HS256")
        return {"token": token}

        return redirect("/artwork/" + str(id_artwork))
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/user/<int:id_user_owner>/block", methods=["GET"])
def get_block_by_id_user_owner(id_user_owner):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        blocks = cursor.execute(
            """ select "index", previous_hash, data, "timestamp", hash, nonce from block
            WHERE id_user_owner = ? """,
            [id_user_owner],
        ).fetchall()
        if not blocks:
            blocks = []
        return jsonify(blocks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/user/<int:id_user_owner>/block/<int:id_block>", methods=["GET"])
def get_block_by_id_user_owner_and_id_block(id_user_owner, id_block):
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        block = cursor.execute(
            """ select "index", previous_hash, data, "timestamp", hash, nonce from block
            WHERE id_user_owner = ? and id= ? """,
            [id_user_owner, id_block],
        ).fetchone()
        if not block:
            block = {}
        return jsonify(block)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/creator", methods=["GET"])
def get_all_creator():
    connect = sqlite3.connect("./database.db")
    connect.row_factory = dict_factory
    try:
        cursor = connect.cursor()
        creators = cursor.execute(
            """ select DISTINCT (b.id_user_owner), pseudo from block b INNER JOIN user u  
            ON b.id_user_owner = u.id """,
        ).fetchall()
        if not creators:
            creators = []
        return jsonify(creators)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route('/')
def index():
    return render_template('index.html')

app.run()
