from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import os.path

from variables import constants



engine   = None
metadata = None



# -----------------------------------------------------------------------------
# Name: connectToDBFile
# Abstract: Connects to the database file and stores the engine variable
# -----------------------------------------------------------------------------
def connectToDBFile( ):

    global engine

    # Create the DB Engine and get an engine variable
    engine = create_engine( constants.DB_URI )

# End connectToDBFile( )



# -----------------------------------------------------------------------------
# Name: createMetaData
# Abstract: Creates a metadata variable so we can create schemas to send 
#           them to the DB
# -----------------------------------------------------------------------------
def createMetaData( ):

    global metadata
    global engine

    # Create a new metadata variable
    metadata = MetaData( )

# End createMetaData( )



# -----------------------------------------------------------------------------
# Name: initializeDB
# Abstract: Initializes the database with the base tables used to store data
# -----------------------------------------------------------------------------
def initializeDB( ):

    global metadata
    global engine

    # First we need to connect to the database
    connectToDBFile( )

    # Next we need a metadata variable
    createMetaData( )

    # Define a table
    students = Table( 'students', metadata, 
        Column( 'id',       Integer, primary_key = True ), 
        Column( 'name',     String                      ), 
        Column( 'lastname', String                      )
    ) # End students

    # Finally, create the schema
    metadata.create_all( engine )

# End initializeDB( )



# -----------------------------------------------------------------------------
# Name: connectToDB
# Abstract: Checks if the db file exists. If not, it attempts to create the 
#           file and initialize it with tables
# -----------------------------------------------------------------------------
def connectToDB( ):

    # Does the db already exist?
    if database_exists( constants.DB_URI ) == False:

        # No, first create it
        create_database( constants.DB_URI )

        # Then initialize it with a schema
        initializeDB( )

    # End if

# End connectToDB( )



# -----------------------------------------------------------------------------
# Name: disconnectDB
# Abstract: Disconnects from the database
# -----------------------------------------------------------------------------
def disconnectDB( ):

    global engine

    if engine is not None:

        engine.dispose( )

# End disconnectDB( )



# Run the main method
if __name__ == '__main__':

    connectToDB( )

# End if