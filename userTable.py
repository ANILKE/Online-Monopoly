import sqlite3
def start():
    conn = sqlite3.connect('users.db')

    # Create a table for storing user credentials
    conn.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(255),email VARCHAR(255),name VARCHAR(255), password VARCHAR(255))')

    # Add a sample user to the table
    try:
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser1','test1@gmail.com','anil', 'testpassword1')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser2','test2@gmail.com','anil', 'testpassword2')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser3','test3@gmail.com','anil', 'testpassword3')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser4','test4@gmail.com','anil', 'testpassword4')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser5','test5@gmail.com','anil', 'testpassword5')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser6','test6@gmail.com','anil', 'testpassword6')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser7','test7@gmail.com','anil', 'testpassword7')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser8','test8@gmail.com','anil', 'testpassword8')")
        conn.execute("INSERT INTO users (username,email,name, password) VALUES ('testuser9','test9@gmail.com','anil', 'testpassword9')")
    except Exception as e:
        print(e)
        pass   

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()
    #Connect to the database file

def cokkie_owner(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Check if the user exists in the database
    sql_query = "SELECT * FROM users WHERE username = ?"

    # define the values to be inserted as a tuple
    values = (username,)

    # execute the SQL query and commit the changes to the database
    result = cursor.execute(sql_query, values).fetchone()
    #result = conn.execute("SELECT * FROM users WHERE username = ? ", (username,)).fetchone()

    # Close the database connection
    conn.close()

    # If the user exists in the database, return True, otherwise return False
    return result
# Now let's implement the login functionality
def login(username, password):
    # Connect to the database file
    conn = sqlite3.connect('users.db')

    # Check if the user exists in the database
    result = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()

    # Close the database connection
    conn.close()

    # If the user exists in the database, return True, otherwise return False
    return result


# Register a new user. 
def register(username, email, name, password):
    # If there is a user with the same username, return False
    if cokkie_owner(username):
        return False,'username already exists'
    
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(255),email VARCHAR(255),name VARCHAR(255), password VARCHAR(255))')

    try:
        conn.execute("INSERT INTO users (username,email,name, password) VALUES (?,?,?,?)",(username,email,name,password))
    except Exception as e:
        print(e)
        return False,'error while inserting'
    
    conn.commit()
    conn.close()
    
    
    
    return True,''
    


# Test the login functionality

# print(login('testuser1', 'testpassword1')) # Output: True
# print(login('testuser', 'testpassword1')) # Output: False
# print(login('testuser2', 'wrongpassword1')) # Output: False
# print(login('testuser2', 'testpassword2')) # Output: False
# print(login('testuser6', 'testpassword6')) # Output: False