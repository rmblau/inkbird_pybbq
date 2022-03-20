import sqlite3

from variables import global_vars


connection = None
cursor = None


# -----------------------------------------------------------------------------
# Name: createConnection
# Abstract: Create a connection to the database file
# -----------------------------------------------------------------------------
def createConnection():
    print(global_vars.DB_PATH)

    # Create the connection
    connection = sqlite3.connect(global_vars.DB_PATH)

    return connection

# End createConnection( )


# -----------------------------------------------------------------------------
# Name: createCursor
# Abstract: Create a cursor using the connection
# -----------------------------------------------------------------------------
def createCursor():

    # Create a cursor
    cursor = createConnection().cursor()

    return cursor

# End createCursor( )


# -----------------------------------------------------------------------------
# Name: createConnectToDatabase
# Abstract: Calls both createConnection and createCursor. This will create the
#           database file and connect to it if it exists. If it already exists,
#           it will simply connect to it.
# -----------------------------------------------------------------------------
def createConnectToDatabase():

    # Create a connection
    createConnection()

    # Create the cursor
    createCursor()

# End createConnectToDatabase( )
