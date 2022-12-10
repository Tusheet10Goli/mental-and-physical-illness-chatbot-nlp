from flask import Flask, jsonify, request
import psycopg2
import uuid
import sys
import os
import platform
CURR_FILE = os.path.abspath(__file__)
CURR_DIR = CURR_FILE[:CURR_FILE.rfind('/') + 1]
if platform.system() == 'Windows':
    CURR_DIR = CURR_FILE[:CURR_FILE.rfind('\\') + 1]
sys.path.append(CURR_DIR)
from response_builder import build_response


app = Flask(__name__)
user_id = 0


@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({'STATUS': 'ACTIVE', 'METHOD': 'health-check'})


@app.route('/send-message', methods=['GET', 'POST'])
def send_message():
    conn, cursor = get_connection()
    data = request.get_json()
    message = data['message']
    responses = build_response(message)
    pip_response = responses['pip'][0]
    mip_response = responses['mip'][0]
    response = None
    if pip_response is None or len(pip_response) == 0: 
        response = f'Your predicted mental illness risk is: {mip_response}'
    else: 
        response = pip_response
    query = 'INSERT INTO chat VALUES (%s, %s, %s);'
    cursor.execute(query, [user_id, message, response])
    close_connection(conn, cursor)
    return jsonify({'STATUS': 'ACTIVE', 'METHOD': 'send-message', 'RESPONSE': response})


@app.route('/authenticate-user/<email>/<password>', methods=['GET'])
def authenticate_user(email, password):
    global user_id
    conn, cursor = get_connection()
    query = 'SELECT user_id, email, password FROM users WHERE email=%s AND password=%s;'
    cursor.execute(query, [email, password])
    user = cursor.fetchone()
    close_connection(conn, cursor)
    if not user:
        return jsonify({'STATUS': 'ERROR', 'METHOD': 'authenticate-user', 'MESSAGE': 'Invalid user email and/or password'})
    user_id = user[0]
    return jsonify({'STATUS': 'ACTIVE', 'METHOD': 'authenticate-user', 'MESSAGE': 'User Logged In!'})


@app.route('/register-user', methods=['POST'])
def register_user():
    conn, cursor = get_connection()
    data = request.get_json()
    user_id = str(uuid.uuid4())
    fname = data['fname']
    mname = data['mname']
    lname = data['lname']
    dob = data['dob']
    gender = data['gender']
    email = data['email']
    password = data['password']
    query = 'INSERT INTO users (user_id, fname, mname, lname, dob, gender, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
    cursor.execute(query, [user_id, fname, mname, lname, dob, gender, email, password])
    close_connection(conn, cursor)
    return jsonify({'STATUS': 'ACTIVE', 'METHOD': 'register-user', 'RESPONSE': 'User Is Registered!', 'USER_ID': user_id})


@app.route('/get-user-data', methods=['GET'])
def get_user_data():
    global user_id
    conn, cursor = get_connection()
    query = 'SELECT * FROM users WHERE user_id=%s;'
    cursor.execute(query, [user_id])
    user_data = cursor.fetchone()
    close_connection(conn, cursor)
    return jsonify({'STATUS': 'ACTIVE', 'METHOD': 'get-user-data', 'RESPONSE': user_data})


def get_connection():
    conn = psycopg2.connect(
        host="ec2-3-209-61-239.compute-1.amazonaws.com",
        database='d9dol0u4tdoh24',
        user='upgypwamervwra',
        password='155ada4c4d305e58202abd7d24a0047354827be2c690b0a1696956c926532497'
    )
    cursor = conn.cursor()
    conn.autocommit = True
    return conn, cursor


def close_connection(conn, cursor):
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run()
