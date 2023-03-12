from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re
from datetime import datetime
import os
import pymysql
import json

DB_USER = 'root'
DB_PASS= '1q2w3eASD123'
DB_NAME = 'user_data'
INSTANCE_CONNECTION_NAME = 'python-discord-bot-371723:us-east4:discord-user-info'

app = Flask(__name__)


def open_connection():
    unix_socket = '/cloudsql/{}'.format(INSTANCE_CONNECTION_NAME)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            con = pymysql.connect(user=DB_USER, password=DB_PASS, unix_socket=unix_socket, db=DB_NAME, cursorclass=pymysql.cursors.DictCursor)
    except:
        print(e)
    conn = con
    cursor = conn.cursor()
    return conn, cursor

@app.route('/receive/formdata/', methods=['POST'])
def receive():
    conn, cursor = open_connection()
    
    details = request.get_json()
    username = details["What's your Discord username?"][0]

    identifier = username[-4:]
    username = username[:-5]

    print(username)
    print(identifier)
    
    query = "INSERT INTO `user_data`.`user_data` (`username`, `name`, `email`, `color`, `hobby`,`screamtime`, `num`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {})".format(details.get("What's your Discord username?")[0], details.get("What's your First & Last Name?")[0],details.get("Enter your email")[0],details.get("Pick your favorite color (out of the options below -.-)")[0],details.get("Choose your favorite hobby")[0],details.get("If you wanted to scream at the world (spew venom, hurl insults, anything works these days :)), what time would you choose.")[0],details.get("Enter a number (integer) between 1 and 1000.")[0])
        
    cursor.execute(query)
    conn.commit()
    
    conn.close()
    # datetime object containing current date and time
    print('https://discordapp-3k67fj2ffa-uk.a.run.app/register_user/'+username+'/'+identifier)
    return redirect('https://discordapp-3k67fj2ffa-uk.a.run.app/register_user/'+username+'/'+identifier)

@app.route('/test/', methods=['GET'])
def receive_test():
    return redirect('https://www.khanacademy.org/')

"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
"""
