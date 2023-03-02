# import pytest
# import uuid
# import mysql.connector
# from api.app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_create_user_profile_field(client):
#     # Connect to the MySQL database
#     conn = mysql.connector.connect(
#         host='0.0.0.0',
#         user='flaskcreds',
#         password='F4kePlasticTrees#',
#         database='test_a12y'
#     )
    
#     # Create a cursor object to interact with the database
#     cursor = conn.cursor()

#     # Delete any existing test data
#     cursor.execute("DELETE FROM user_profile_fields WHERE name = 'Test Field'")

#     # Make a POST request to create a new user profile field
#     response = client.post('/profile-fields', json={
#         'name': 'Test Field',
#         'data_type': 'string'
#     })

#     # Verify that the response is successful and contains the expected data
#     assert response.status_code == 201
#     # assert response.json == {'id': str(uuid.UUID(bytes=response.json['id']))}

#     # Execute a SELECT statement to retrieve the newly created field
#     select_query = """
#         SELECT name, data_type
#         FROM user_profile_fields
#         WHERE name = 'Test Field'
#     """
#     cursor.execute(select_query)
#     field = cursor.fetchone()

#     # Verify that the field exists in the database and has the expected data
#     # assert field[1] is not None
#     # assert field == 'Test Field'
#     # assert field[2] == 'string'

#     # Close the connection to the database
#     conn.close()

# @pytest.mark.parametrize('data_type, value, expected', [
#     ('string', 'Test Value', 'Test Value'),
#     ('int', 123, '123'),
#     ('float', 1.23, '1.23'),
#     ('bool', True, 'True'),
#     ('date', '2022-01-01', '2022-01-01')
# ])
# def test_create_user_profile(client, data_type, value, expected):
#     # Connect to the MySQL database
#     conn = mysql.connector.connect(
#         host='0.0.0.0',
#         user='flaskcreds',
#         password='F4kePlasticTrees#',
#         database='test_a12y'
#     )

#     # Create a cursor object to interact with the database
#     cursor = conn.cursor()

#     # Delete any existing test data
#     cursor.execute("DELETE FROM user_profiles WHERE user_id = 'testuser'")

#     # Create a new user profile field for the test
#     cursor.execute("""
#         INSERT INTO user_profile_fields
#         (name, data_type)
#         VALUES
#         ('Test Field', %s)
#     """, (data_type,))
#     field_id = cursor.lastrowid

#     # Make a POST request to create a new user profile
#     response = client.post('/users/testuser/profile', json={
#         'field_id': field_id,
#         'value': value
#     })

#     # Verify that the response is successful and contains the expected data
#     assert response.status_code == 201
#     assert response.json == {'id': str(uuid.UUID(bytes=response.json['id']))}

#     # Execute a SELECT statement to retrieve the newly created profile
#     select_query = """
#         SELECT field_id, value
#         FROM user_profiles
#         WHERE user_id = 'testuser' AND field_id = %s
#     """
#     cursor.execute(select_query, (field_id,))
#     profile = cursor.fetchone()

#     # Verify that
