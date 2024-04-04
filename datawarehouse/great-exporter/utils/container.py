import os
from .configloader import Config
from .exportutils import intialize_engine
from .dbutils import DatabaseManager
from sqlalchemy import Table

class Container:
    def __init__(self, root_dir: str, list_of_loaders: list[type], schemas: dict[str, Table] = {}):
        self.root_dir        = root_dir
        self.list_of_loaders = list_of_loaders
        self.schemas         = schemas
        self.initialize()

    def get_table(self, name: str, db_name: str):
        return self.dbs.get_table(name, db_name)
    
    def initialize(self):
        self.config = Config(os.path.join(self.root_dir, 'config.json'))
        self.config.loadConfig()

        self.engine = intialize_engine(self.config.destination_db)
        self.dbs    = DatabaseManager(self.config.source_databases)

        
        