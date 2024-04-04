import pandas as pd
from sqlalchemy import Table, Engine
from .container import Container
from .dbutils import DatabaseManager

class SourceTable:
    def __init__(self, db_name: str, schema: Table):
        self.db_name = db_name
        self.name    = schema.name
        self.schema  = schema

class Dependencies:
    source_tables: list[str]
    destination_tables: list[str]

    def __init__(self, source_tables: list[str] = [], destination_tables: list[str] = []):
        self.source_tables      = source_tables
        self.destination_tables = destination_tables

class DWTableLoader:
    engine: Engine
    dbs:    DatabaseManager

    def __init__(self, container: Container, schema_name: str, source_tables: dict[str, SourceTable], insert_dependencies: Dependencies = Dependencies(), update_dependencies: Dependencies = Dependencies()) -> None:
        self.container = container
        self.engine    = container.engine
        self.dbs       = container.dbs

        self.source_tables       = source_tables
        self.destination_table   = container.schemas[schema_name]
        self.insert_dependencies = insert_dependencies
        self.update_dependencies = update_dependencies



    def load_source_tables(self) -> dict[str, pd.DataFrame]:
        tables: dict[str, pd.DataFrame] = {}
        for table in self.source_tables.values():
            tables[table.name] = self.dbs.get_table(table.name, table.db_name)

        return tables
    
    def initialLoad(self) -> pd.DataFrame:
        raise NotImplementedError
    
