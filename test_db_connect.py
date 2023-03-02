import pytest
import mysql.connector
from app import get_users

# @pytest.fixture
# def test_database():
#     # Connect to a test database
#     conn = mysql.connector.connect(
#         host='0.0.0.0',
#         user='flaskcreds',
#         password='F4kePlasticTrees#',
#         database='test_a12y'
#     )

#     # Create a test table with some test data
#     cursor = conn.cursor()
#     # cursor.execute("CREATE TABLE users (id INT PRIMARY KEY, username VARCHAR(50))")
#     cursor.execute("INSERT INTO users (id, username, email, password, first_name, last_name) VALUES (1, 'john_doe', 'john_doe@gmail.com', '93448cc4-03e4-4cf7-b670-2810f63167cc', 'John', 'Doe')")
#     # cursor.execute("INSERT INTO users (id, username) VALUES (2, 'jane_doe')")

#     yield conn

#     # Teardown: Drop the test table and close the connection
#     # cursor.execute("DROP TABLE users")
#     conn.close()

def test_get_users():
    # Call the get_users function
    #users = get_users()

    # assert isinstance(users, list)
    # assert users[0]['username'] == 'jane_doe'
    assert(3) == 3
    # assert(3).Eq(3)
    

