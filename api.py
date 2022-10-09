from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3366
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'ksalf'
app.config['MYSQL_DB'] = 'social_network'
 
mysql = MySQL(app)

@app.route("/run_migration")
def run_migration():
    cursor = mysql.connection.cursor()
    with open('init_db.sql', 'r') as f:
        cursor.execute(f.read())
    cursor.close()
    return "Have successfully executed initial migration!"