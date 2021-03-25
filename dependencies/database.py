# Common module to provide database support to application
# Uses MongoEngine as ORM to connect to MongoDB instance managed with pods
# It is provided as a Context Manager e.g. with open(<fileName>) as handle:
from mongoengine import connect


# Context Manager for database
class DatabaseHandler:
    ''' Handles database request i.e. all CRUD operations '''

    # Define initialization codes
    def __init__(self, settings):
        '''
        Use mongoEngine Connect to connect to database sources.
        Basic connection parameteres:
        Connect("<document name>")
        '''
        self.db = connect(settings.db_name,
                          host=settings.db_host,
                          port=settings.db_port,
                          username=settings.db_username,
                          password=settings.db_password,
                          authentication_source=settings.db_auth_source,
                          alias='default'
                          )

    # Define actual dependencies for yield
    def __enter__(self):
        return self.db

    # Define garbage collection
    def __exit__(self):
        self.db.disconnect()


# Defines a Context Dependencies
async def get_database(settings):
    with DatabaseHandler(settings) as db:
        yield db
