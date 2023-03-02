from flask import Flask, request, jsonify, session
from flask_cors import CORS
import bcrypt

import uuid
import mysql.connector

app = Flask(__name__)
CORS(app)

# changed mydb to conn
conn = mysql.connector.connect(
  host="mysql",
  user="myuser",
  password="mypassword",
  database="a12y"
)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_all_users():
    # Create a cursor object
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    cur = conn.cursor()

    try:
        # Query the database for all users
        cur.execute("SELECT id, username, email, first_name, last_name, bio, avatar_url, total_karma_points, created_at, updated_at FROM users")
        rows = cur.fetchall()
        cur.close

        # Create a list of dictionaries containing the user data
        user_data = []
        for row in rows:
            user_data.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'first_name': row[3],
                'last_name': row[4],
                'bio': row[5],
                'avatar_url': row[6],
                'total_karma_points': row[7],
                'created_at': row[8].strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': row[9].strftime('%Y-%m-%d %H:%M:%S')
            })

        # Return the user data as a JSON response
        return jsonify(user_data)
    except:
        # Roll back the transaction if an error occurs
        conn.rollback()
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/users/<string:username>', methods=['GET'])
def get_user_by_username(username):
    # connect to the MySQL database
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    # create a cursor object to interact with the database
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,) )
    result = cursor.fetchone()
    
    username, password = result
    return jsonify({'username': username, 'password': password}), 200

@app.route('/users', methods=['POST'])
def create_new_user():
    # Create a cursor object
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    # Get the user data from the request
    user_data = request.get_json()

    # Create a cursor object
    cur = conn.cursor()

    try:
        # Check if the email or username already exist in the database
        cur.execute("SELECT * FROM users WHERE email = %s OR username = %s", (user_data['email'], user_data['username']))
        existing_user = cur.fetchone()

        if existing_user:
            # Return an error message if the email or username already exist
            return jsonify({'error': 'Email or username already exist'}), 400

        # Generate a new UUID for the user ID
        user_id = uuid.uuid4()

        # Insert the new user into the database
        cur.execute("INSERT INTO users (id, username, email, password, first_name, last_name, bio, avatar_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (str(user_id), user_data['username'], user_data['email'], user_data['password'], user_data['first_name'], user_data['last_name'], user_data['bio'], user_data['avatar_url']))

        # Commit the transaction
        conn.commit()

        # Return the new user data
        return jsonify({'id': user_id, 'username': user_data['username'], 'email': user_data['email'], 'first_name': user_data['first_name'], 'last_name': user_data['last_name'], 'bio': user_data['bio'], 'avatar_url': user_data['avatar_url']}), 201
    except:
        # Roll back the transaction if an error occurs
        conn.rollback()
    finally:
        # Close the cursor object
        cur.close()

    # Close the connection object (not needed if using SQLAlchemy)
    conn.close()
    return jsonify({'error': 'An error occurred'}), 500

@app.route('/profile-fields', methods=['GET'])
def get_all_profile_fields():
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    cursor = conn.cursor()
    # execute a SELECT statement to retrieve all profile fields
    select_query = "SELECT * FROM user_profile_fields"
    
    try:
        cursor.execute(select_query)

    # fetch all rows as a list of dictionaries
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(rows), 200

    finally:
        conn.close()

    # return a JSON response with all profile fields

@app.route('/profile-fields', methods=['POST'])
def create_profile_field():
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )    
    # get the profile field data from the request body
    profile_field_data = request.get_json()

    cursor = conn.cursor()

    # execute the INSERT statement to create a new profile field
    insert_query = """
        INSERT INTO user_profile_fields
        (name, data_type)
        VALUES
        (%s, %s)
    """
    field_data = (profile_field_data['name'], profile_field_data['data_type'])
    
    try:
        cursor.execute(insert_query, field_data)
        conn.commit()
    except:
        # Roll back the transaction if an error occurs
        conn.rollback()
    finally:
        # Close the cursor object
        cursor.close()
        
    # commit the changes and close the cursor
    conn.close()

    # return a JSON response with the ID of the new profile field
    response_data = {'id': cursor.lastrowid}
    return jsonify(response_data), 201

@app.route('/profiles', methods=['POST'])
def create_profile():
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    # get the profile data from the request body
    profile_data = request.get_json()

    # generate a new UUID for the profile
    profile_id = uuid.uuid4()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO user_profiles (id, user_id, field_id, value) VALUES(%s, %s, %s, %s)
    """
    profile_data = (str(profile_id), profile_data['user_id'], profile_data['field_id'], profile_data['value'])
    
    try:
        cursor.execute(insert_query, profile_data)
        # commit the changes and close the cursor
        conn.commit()
    except:
        conn.rollback()
        return jsonify({'error': 'An error occurred', 'debuginfo': profile_data}), 400
    finally:
        cursor.close()

    conn.close()
    # return a JSON response with the ID of the new profile
    response_data = {'id': str(profile_id)}
    return jsonify(response_data), 201

@app.route('/users/<user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    
    # connect to the MySQL database
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    # create a cursor object to interact with the database
    cursor = conn.cursor()

    # execute a SELECT statement to retrieve the user's profile
    select_query = """
        SELECT f.name, p.value
        FROM user_profiles p
        INNER JOIN user_profile_fields f ON f.id = p.field_id
        WHERE p.user_id = %s
    """
    
    try:
        cursor.execute(select_query, (user_id,))
        # fetch all rows as a list of dictionaries
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()    
        
        
    # close the connection and return the list of profiles
    conn.close()
    return jsonify(rows), 200

@app.route('/login', methods=['POST'])
def signin():
    
    # connect to the MySQL database
    conn = mysql.connector.connect(
        host="mysql",
        user="myuser",
        password="mypassword",
        database="a12y"
    )
    # create a cursor object to interact with the database
    cursor = conn.cursor()
    username = request.json.get('username')
    
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,) )
    result = cursor.fetchone()
    
    username, password = result
    return jsonify({'username': username, 'password': password}, 200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
