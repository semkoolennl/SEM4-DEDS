import json
from typing import Any
from schema import Schema, Or # type: ignore
from .config import ConnectionConfig, SourceCSVDatabase, SourceSQLite3Database

config_schema = Schema({
    '$schema': 'utils/config.schema.json',
    'DESTINATION_DB': {
        'host': str,
        'port': int,
        'database': str,
        'username': str,
        'password': str,
        'driver': str,
        'dialect': str
    },
    'SOURCE_DATABASES': [
        Or({
            'name': str,
            'type': 'csv',
            'path': str,
            'delimiter': str,
            'colcount': int,
        }, {
            'name': str,
            'type': 'sqlite',
            'path': str
        })
    ]
})


class Config:
    destination_db: ConnectionConfig
    source_databases: dict[str, SourceSQLite3Database|SourceCSVDatabase]

    def __init__(self, config_file: str):
        self.config_file = config_file

    def loadConfig(self) -> None:
        print(f"--- Loading config file: {self.config_file}")
        data = json.load(open(self.config_file))
        self.validateSchema(data)
        self.loadDestinationDB(data['DESTINATION_DB'])     
        self.loadSourceDatabases(data['SOURCE_DATABASES'])

    def validateSchema(self, data: dict[str, Any]) -> None:
        print("--- Validating config file schema")
        try:
            config_schema.validate(data) # type: ignore
        except Exception as e:
            raise ValueError(f"Invalid config file: {e}")
    
    def loadDestinationDB(self, data: dict[str, Any]) -> None:
        print("--- Loading destination database configuration")
        self.destination_db = ConnectionConfig(
            host     = data['host'],
            port     = data['port'],
            database = data['database'],
            username = data['username'],
            password = data['password'],
            driver   = data['driver'],
            dialect  = data['dialect']
        )

    def loadSourceDatabases(self, data: list[dict[str, Any]]) -> None:
        print("--- Loading source databases configurations")
        self.source_databases = {}
        for db_info in data:
            if db_info['type'] == 'csv':
                self.source_databases[db_info['name']] = self.loadCSVDatabase(db_info)
            elif db_info['type'] == 'sqlite':
                self.source_databases[db_info['name']] = self.loadSQLite3Database(db_info)
            else:
                raise ValueError(f"Unsupported database type: {db_info['type']}")
            
    def loadSQLite3Database(self, db_info: dict[str, Any]) -> SourceSQLite3Database:
        print(f"--- Loading SQLite3 database config: {db_info['name']}")

        return SourceSQLite3Database(db_info['name'], db_info['path'])

    def loadCSVDatabase(self, db_info: dict[str, Any]) -> SourceCSVDatabase:
        print(f"--- Loading CSV database config: {db_info['name']}")

        return SourceCSVDatabase(db_info['name'], db_info['path'], db_info['delimiter'], db_info['colcount'])
    
    def __repr__(self) -> str:
        source_dbs = "\n".join([f"{db}" for db in self.source_databases.values()])
        yellow_BG  = "\033[43m"
        reset      = "\033[0m"
        return (
            f"\n{yellow_BG}ConfigLoader data:{reset}\n"
            f"{self.destination_db}\n"
            f"{source_dbs}"
        )
        