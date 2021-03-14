# Common module to provide database support to application
# Uses MongoEngine as ORM to connect to MongoDB instance managed with pods
# It is provided as a Context Manager e.g. with open(<fileName>) as handle:
from mongoEngine import connect


# Context Manager for database
class DatabaseHandler:
    ''' Handles database request i.e. all CRUD operations '''

    # Define initialization codes
    def __init__(self):
        '''
        Use mongoEngine Connect to connect to database sources.
        Basic connection parameteres:
        Connect("<document name>")
        '''
        self.db = connect('guides',
                          host='127.0.0.1',
                          port=27017,
                          username='guide',
                          password='GuideAdmin',
                          authentication_source='admin'
                          )

    # Define actual dependencies for yield
    def __enter__(self):
        return self.db

    # Define garbage collection
    def __exit__(self):
        self.db.disconnect()


# Defines a Context Dependencies
async def get_database():
    with DatabaseHandler() as db:
        yield db
