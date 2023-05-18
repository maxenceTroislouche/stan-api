"""
    Pour executer le code : 
    - Lancer la venv : .env/bin/activate
    - uvicorn index:app
"""

from fastapi import FastAPI
from db import DatabaseConnection
app = FastAPI()

@app.get("/")
def index():
    return {
        "message": "OK"
    }

@app.get("/user/{user_id}")
def get_user_info(user_id: int):
    query = f"SELECT id, lastname, firstname, isadmin, passcode, fingerprint_eigenvalue FROM user WHERE id = {user_id}"
    db = DatabaseConnection()
    result_array = db.execute_select(query)

    return_dict = {}

    if len(result_array) == 0:
        return {
            "ERROR": "NOT FOUND"
        }

    for user in result_array:
        return_dict = {
            'id': user[0],
            'lastname': user[1],
            'firstname': user[2],
            'isadmin': user[3],
            'passcode': user[4],
            'fingerprint_eigenvalue': user[5]
        }

    return return_dict


@app.post('/user')
def create_new_user(lastname: str, firstname: str, isadmin: bool, passcode: str, fingerprint_eigenvalue: str):
    query = f"INSERT INTO user (lastname, firstname, isadmin, passcode, fingerprint_eigenvalue) VALUES ('{lastname}', '{firstname}', {isadmin}, '{passcode}', '{fingerprint_eigenvalue}')"
    print(query)
    db = DatabaseConnection()
    db.execute_query(query)

    return {
        'message': 'OK'
    }

@app.put('/user/{user_id}')
def update_user(user_id: int, lastname: str, firstname: str, isadmin: bool, passcode: str, fingerprint_eigenvalue: str):
    query = f"UPDATE user SET lastname = '{lastname}', firstname = '{firstname}', isadmin = {isadmin}, passcode = '{passcode}', fingerprint_eigenvalue = '{fingerprint_eigenvalue}' WHERE id = {user_id}"
    db = DatabaseConnection()
    db.execute_query(query)

    return {
        'message': 'OK'
    }

@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    query = f"DELETE FROM user WHERE id = {user_id}"
    db = DatabaseConnection()
    db.execute_query(query)

    return {
        'message': 'OK'
    }

@app.get('/stan/{stan_id}')
def get_stan_data(stan_id: int):
    query = f"SELECT id, mode, idconnecteduser, position FROM stan_device WHERE id = {stan_id}"
    db = DatabaseConnection()
    result_array = db.execute_select(query)

    if len(result_array) == 0:
        return {
            'ERROR': 'NOT FOUND'
        }

    return_dict = {}
    for stan in result_array:
        return_dict = {
            'id': stan[0],
            'mode': stan[1],
            'idconnecteduser': stan[2],
            'position': stan[3]
        }

    return return_dict

@app.put('/stan/connectuser')
def connect_user_to_stan(id_stan: int, id_user: int):
    # On vérifie si le user existe
    user_info = get_user_info(id_user)
    if 'ERROR' in user_info.keys():
        return {"ERROR": "USER DOESN'T EXIST"}

    # On vérifie si le stan existe 
    stan_info = get_stan_data(id_stan)
    if 'ERROR' in stan_info.keys():
        return {"ERROR": "STAN DOESN'T EXIST"}

    # On vérifie si le stan possède pas déjà un user
    if stan_info["idconnecteduser"] is None:
        return {"ERROR": "STAN ALREADY USED"}

    # On vérifie si le user est pas déjà connecté à un stan
    query = f"SELECT id FROM stan_device WHERE idconnecteduser = {id_user}"
    db = DatabaseConnection()
    result_array = db.execute_select(query)

    for x in result_array:
        return {"ERROR": "USER ALREADY CONNECTED TO ANOTHER STAN"}

    # On connecte le user au stan
    query = f"UPDATE stan_device SET idconnecteduser = {id_user} WHERE id = {id_stan}"
    db.execute_query(query)
    return {
        'message': 'OK'
    }

@app.put('/stan/disconnectuser')
def disconnect_user_from_stan(id_stan: int):
    query = f"UPDATE stan_device SET idconnecteduser = NULL WHERE id = {id_stan}"
    db = DatabaseConnection()
    db.execute_query(query)
    return {
        'message': 'OK'
    }

"""
Endpoints:
    - GET / (test)

    - GET /user/id
    - POST /user
    - PUT /user
    - DELETE /user

    - GET /stan/id
    - PUT /stan/connectuser
    - PUT /stan/disconnectuser
    (Reste fait à la mano)
"""