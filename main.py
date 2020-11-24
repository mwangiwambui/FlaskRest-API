from flask import Flask, request, jsonify

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'students'

# Intialize MySQL
mysql = MySQL(app)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route("/api/search_student", methods=['GET'])
def search_student():
    query_parameters = request.args
    student_no = query_parameters.get('student_no')

    if not student_no:
        return page_not_found(404)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE student_number = %s', (student_no,))
    student = cursor.fetchone()
    return jsonify(student)


@app.route("/api/get_students", methods=['GET'])
def get_student():
    query = "SELECT * FROM users"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)


@app.route("/api/add_student", methods=['POST'])
def add_student():
    req_data = request.get_json()
    username = req_data['username']
    email = req_data['email']
    address = req_data['address']
    class_details = req_data['class_details']
    student_no = req_data['student_no']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE student_number = %s', (student_no,))
    account = cursor.fetchone()

    if account:
        return 'User already exists!'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return 'Invalid email address!'
    elif not re.match(r'[A-Za-z0-9]+', username):
        return 'Username must contain only characters and numbers!'
    elif not username or not student_no or not email:
        return 'Please fill out the form!'
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)',
                       (username, email, address, class_details, student_no))
        mysql.connection.commit()
        return "Data successfully saved"


if __name__ == '__main__':
    app.run(debug=True)
