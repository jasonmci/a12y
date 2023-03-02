from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
mydb = mysql.connector.connect(
  host="mysql",
  user="myuser",
  password="mypassword",
  database="a12y"
)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users')
def users():
    # Query the database for all users
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Convert users to a JSON response
    response = []
    for user in users:
        response.append({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
