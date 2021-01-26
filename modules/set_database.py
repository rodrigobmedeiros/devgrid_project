import json

class SetDatabase():
    """
    class responsible to load database configuration from config.json file.
    """
    def __init__(self):
        
        self.database = None
        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.database_name = None
        self.read_config_file()

    def read_config_file(self):

        with open('./config.json') as config_file:

            config_info = json.load(config_file)

        database_info = config_info["database_info"]

        self.database = database_info['database']
        self.user = database_info['user']
        self.password = database_info['password']
        self.host = database_info['host']
        self.port = database_info['port']
        self.database_name = database_info['database_name']

        return None

    def get_database_string(self):

        db_string = ''.join([self.database, 
                             '://',
                             self.user,
                             ':',
                             self.password,
                             '@',
                             self.host,
                             ':',
                             self.port, 
                             '/',
                             self.database_name])

        return db_string