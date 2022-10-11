from flask import Flask, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3366
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'ksalf'
app.config['MYSQL_DB'] = 'social_network'
 
mysql = MySQL(app)


@app.route("/register", methods = ['POST'])
def register():
    data = request.get_json()
    login, password = data["login"], data["password"]
    if login and password:
        password_hash = sha256_crypt.encrypt(password)
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO users(login, password) VALUES(%s,%s)''',\
            (login, password_hash))
        mysql.connection.commit()
        cursor.close()
        return "ok", 200


@app.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    login, password = data["login"], data["password"]
    if login and password:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT password FROM users WHERE login = %s''',\
            [login])
        password_hash = cursor.fetchone()[0]
        cursor.close()
        if sha256_crypt.verify(password, password_hash):
            return "ok", 200
        else:
            return "", 401


@app.route("/profile/<user_id>", methods = ['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT 
                name, 
                surname,
                age,
                gender,
                interests,
                city
            FROM profiles WHERE user_id = %s''', [user_id])
        profile = cursor.fetchone()
        cursor.close()
        return { "name": profile[0], "surname": profile[1],
            "age": profile[2], "gender": profile[3],
            "interests": profile[4], "city": profile[5] }, 200
    if request.method == 'POST':
        data = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO 
            profiles(user_id, name, surname, age, gender, interests, city) 
            VALUES(%s,%s,%s,%s,%s,%s,%s)''',\
            (user_id, data["name"], data["surname"], data["age"],\
            data["gender"], data["interests"], data["city"]))
        mysql.connection.commit()
        cursor.close()
        return "ok", 200


@app.route("/run_migration")
def run_migration():
    cursor = mysql.connection.cursor()
    with open('init_db.sql', 'r') as f:
        cursor.execute(f.read())
    cursor.close()
    return "Have successfully executed initial migration!"