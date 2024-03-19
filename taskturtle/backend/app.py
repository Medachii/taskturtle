from flask import *
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from web3 import Web3

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Change to your RPC provider
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
with open('../bin/contracts/TaskManager.json') as f:
    contract_data = json.load(f)
abi = contract_data['abi']
# Replace with your contract address
#/!\ A REMPLACER À CHAQUE FOIS
contract_address = '0x869017bb0668AEcdAF6cde3EABce6251233B427B'

contract = w3.eth.contract(address=contract_address, abi=abi)


CORS(app, supports_credentials=True)


@app.after_request
def refresh_expiring_jwts(response):

    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response .get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        pass
    return response


@app.route('/token', methods=['POST'])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    id_user = cursor.execute(
        "SELECT id FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    if id_user is None:
        return {"msg": "Bad email or password"}, 401
    id_user = id_user[0]

    acces_token = create_access_token(identity=id_user)
    response = {"access_token": acces_token}
    return response


@app.route('/')
def index():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body


@app.route('/profile')
@jwt_required()
def my_profile():
    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    id_user = get_jwt_identity()
    user = cursor.execute(
        "SELECT nom,prenom FROM users WHERE id = ?", (id_user,)).fetchone()
    if user is None:
        return {"msg": "Bad email or password"}, 401
    acceptedtasks = cursor.execute(
        "SELECT * FROM transactions WHERE executant = ?", (id_user,)).fetchall()
    # #print("TRANSACS : ", transacs)
    id_trans = [transac[0] for transac in acceptedtasks]
    createdtasks = cursor.execute(
        "SELECT * FROM transactions WHERE demandeur = ?", (id_user,)).fetchall()
    acceptedtasksinfos = []
    for id_trans in id_trans:
        # #print(cursor.execute("SELECT p.nom, p.description, u.nom, u.prenom, p.note FROM projets p JOIN users u ON p.id_auteur = u.id WHERE p.id = ?", [id]).fetchall())
        (a, b, c, d, e,f,g,h) = cursor.execute(
            "SELECT t.nom, t.description, u.nom, u.prenom, t.note,t.prix,t.accepted,t.completed FROM transactions t JOIN users u ON t.demandeur = u.id WHERE t.id_transaction = ?", [id_trans]).fetchall()[0]
        acceptedtasksinfos.append([id_trans,a, b, c, d, e,f,g,h])
    createdtasksinfos = []
    for (id, nom, desc, demandeur, executant, prix, note, accepted, completed) in createdtasks:
        createdtasksinfos.append([nom, desc, demandeur, executant, prix, id, note, accepted, completed])

    # #print("INFOS : ", infos)
    # #print("TACHES CREES : ", createdtasksinfos)
    # #print("TACHES ACCEPTEES : ", acceptedtasksinfos)
    response_body = {
        "name": ""+user[0] + " " + user[1],
        "acceptedtasks": acceptedtasksinfos,
        "createdtasks": createdtasksinfos
    }
    return response_body


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/list', methods=['GET'])
def list():
    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    list = cursor.execute("SELECT * FROM transactions WHERE accepted = 0 AND completed = 0").fetchall()
    data = []
    for task in list:
        ##print("TASK 3 : ", task[3], " ", type(task[3]))
        demandeur = cursor.execute("SELECT prenom, nom FROM users WHERE id = ?", (task[3],)).fetchone()
        # #print("DEMANDEUR : ", demandeur)
        data.append({"id": task[0], "name": task[1], "description": task[2], "auteur": demandeur[0] + " " + demandeur[1], "prix": task[5], "note": task[6]})

    return json.dumps(data)


@app.route('/add', methods=['POST'])
@jwt_required()
def add():
    #print("On ajoute un slip")
    nom = request.json["nom"]
    desc = request.json["desc"]
    auteur = get_jwt_identity()
    prix = request.json["prix"]
    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    
    list_id = cursor.execute("SELECT MAX(id_transaction) FROM transactions").fetchall()[0]
    #print("LIST_ID : ", list_id)
    if list_id == (None,):
        max_id = 0
    else:
        max_id = list_id[0] + 1

    #print(max_id, nom, desc, auteur, prix)

    cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(max_id, nom, desc, auteur, -1, prix, 0, 0, 0))
    db.commit()
    db.close()

    tx_hash = contract.functions.createTask(int(prix)).transact({"from": w3.eth.accounts[get_jwt_identity()], "value": int(prix)})
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return redirect(url_for('list'))


@app.route('/noter', methods=['POST'])
@jwt_required()
def noter():
    id_projet = int(request.json['idprojet'])
    if request.json['note'] == '':
        note = 0
    else:
        note = int(request.json['note'])

    id_trans = int(request.json['transaction'])

    #print("ID_PROJET : ", id_projet, " ", note, " ", id_trans)

    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    cursor.execute("UPDATE transactions SET note = ? WHERE id_transaction = ?", [
                   note, id_trans])

    notes_projet = cursor.execute(
        "SELECT note FROM transactions WHERE project = ?", [id_projet]).fetchall()
    notes_projet = [p[0] for p in notes_projet]
    #print("NOTES_PROJET : ", notes_projet, " ", type(notes_projet))

    moyenne = sum(notes_projet)/len(notes_projet)
    #print("MOYENNE : ", moyenne)

    cursor.execute("UPDATE projets SET note = ? WHERE id = ?",
                   [moyenne, id_projet])
    #print("NOUVELLE NOTE : ", cursor.execute("SELECT note FROM projets WHERE id = ?", [id_projet]).fetchall())
    db.commit()
    return redirect(url_for('my_profile'))


@app.route('/reservation', methods=['POST'])
@jwt_required()
def reservation():
    #print("On choisit d'exécuter un projet")
    # On récupère l'identity de l'utilisateur
    executant = get_jwt_identity()
    #print("Current user : ", executant)
    trans_id = int(request.json['id'])
    #print("ID TRANSACTION : ", trans_id)

    tx_hash = contract.functions.acceptTask(trans_id).transact({"from": w3.eth.accounts[executant]})

    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    demandeur = cursor.execute("""SELECT demandeur FROM transactions WHERE id_transaction = ?""", (int(trans_id),)).fetchone()[0]
    if executant == demandeur:
        return {"msg": "You can't buy your own project"}, 401
    cursor.execute("""UPDATE transactions SET executant = ? WHERE id_transaction = ?""", (executant, trans_id))
    cursor.execute("""UPDATE transactions SET accepted=1 WHERE id_transaction = ?""",(trans_id,))
    db.commit()
    db.close()
    return {"msg": "Reservation successful"}


@app.route('/createUser', methods=['POST'])
def createUser():
    name = request.json["name"]
    firstname = request.json["firstname"]
    email = request.json["email"]
    password = request.json["password"]
    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()
    list_id = cursor.execute("SELECT MAX(id) FROM users").fetchall()[0]
    if list_id == (None,):
        max_id = 0
    else:
        max_id = list_id[0] + 1
    list_email = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
    if len(list_email) > 0:
        return redirect(url_for('index'))
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                   (max_id+1, name, firstname, email, password, 0))
    db.commit()
    db.close()
    return redirect(url_for('index'))


@app.route('/disconnect', methods=['POST'])
def disconnect():
    session['id'] = None
    return redirect(url_for('index'))


@app.route('/cancel', methods=['POST'])
@jwt_required()
def cancel():
    #print("ID CANCEL AVANT : ", request.json["id"])
    id = int(request.json["id"])
    #print("ID CANCEL : ", id)
    

    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()

    
    completed_flag = cursor.execute("""SELECT completed FROM transactions WHERE id_transaction = ?""", (id,)).fetchone()[0]
    if completed_flag == 1:
        return {"msg": "You can't cancel a project that has been accepted"}, 401
    tx_hash = contract.functions.cancelTask(int(id)).transact({"from": w3.eth.accounts[get_jwt_identity()]})
    cursor.execute("""UPDATE transactions SET accepted = 0  WHERE id_transaction = ?""", (id,))
    cursor.execute("""UPDATE transactions SET completed=1 WHERE id_transaction = ?""", (id,))
    db.commit()
    db.close()
    return {'name': 'CANCEL'}

@app.route('/finalise',methods=['POST'])
@jwt_required()
def finalise():
    id = int(request.json["transaction"])
    
    db = sqlite3.connect('database/projects.db')
    cursor = db.cursor()

    accepted_flag = cursor.execute("""SELECT accepted FROM transactions WHERE id_transaction = ?""", (id,)).fetchone()[0]
    completed_flag = cursor.execute("""SELECT completed FROM transactions WHERE id_transaction = ?""", (id,)).fetchone()[0]
    if completed_flag == 1 or accepted_flag == 0:
        return {"msg": "You can't complete a project that has been completed"}, 401
    tx_hash = contract.functions.completeTask(int(id)).transact({"from": w3.eth.accounts[get_jwt_identity()]})
    cursor.execute("""UPDATE transactions SET completed=1 WHERE id_transaction = ?""", (id,))
    db.commit()
    db.close()
    return {'name': 'FINALISE'}



