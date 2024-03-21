import os
import classconfig
import sqlalchemy
from typing import Iterable 
from utils import Container, DWTableLoader
from utils.exportutils import recreate_db
from schemas import getSchemas, getMeta

class LoaderManager:
    loaders: dict[str, DWTableLoader]
    schemas: dict[str, sqlalchemy.schema.Table]

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.metadata    = getMeta()
        self.schemas     = getSchemas()
        self.container   = Container(self.current_dir, classconfig.get_exporter_classes(), self.schemas)
        
        self.initialize_loaders()
        
    def initialize_loaders(self):
        list_of_loaders = classconfig.get_exporter_classes()
        self.loaders = {}
        for loader in list_of_loaders:
            self.loaders[loader.__name__] = loader(self.container)

    def perform_initial_load(self):
        queue = InsertQueue(self.loaders)

        print("\n\033[42m*** Recreating the database ***\033[0m\n")
        recreate_db(self.container.config.destination_db)

        print("\n\033[42m*** Creating schema ***\033[0m\n")
        for schema in self.schemas.values():
            schema.create(self.container.engine)
            

        for loader in queue:
            dataframe = loader.initialLoad()
            try :
                dataframe.to_sql(loader.destination_table.name, self.container.engine, schema=loader.destination_table.schema, if_exists='append', index=False)
            except Exception as e:
                print(f"\n\033[41m*** Error while loading {loader.destination_table.name} ***\033[0m\n")
                formatted_error = str(e).replace(";", ";\n")
                print(f"\n\033[31m{formatted_error}\033[0m\n")
                exit()
            
        print("\n\033[42m*** Initial load completed ***\033[0m\n")        

# Make this class iterable
class TableLoaderQueue(Iterable[DWTableLoader]):
    queue: list[DWTableLoader] = []
    finished: list[DWTableLoader] = []

    def __init__(self, loaders: dict[str, DWTableLoader]):
        self.loaders = loaders

        self.create_queue()

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.queue) == 0:
            raise StopIteration
        return self.queue.pop(0)

    def create_queue(self):
        pass

        
class InsertQueue(TableLoaderQueue):
    queue:    list[DWTableLoader] = []
    queued_destination_tables: set[str] = set()
    finished: list[DWTableLoader] = []

    def __init__(self, loaders: dict[str, DWTableLoader]):
        self.loaders = loaders

        self.create_queue()
        
    def create_queue(self):
        print("\n\033[42m*** Creating the initial load queue ***\033[0m")

        # Create the queue by looking at the dependencies of the loaders
        current: dict[str, DWTableLoader] = dict(self.loaders)
        next: dict[str, DWTableLoader]    = {}

        loop = 0
        while len(current) > 0 and loop < 100:
            loop += 1
            next = {}
            for name, loader in current.items():
                if self.has_no_unhandled_dependencies(loader):
                    self.queue.append(loader)
                    self.queued_destination_tables.add(loader.destination_table.name)
                else:
                    next[name] = loader
            current = next

        if loop == 100:
            unhappy_loaders_and_dependencies = {loader.__class__.__name__: loader.insert_dependencies.destination_tables for loader in next.values()}
            happy_loaders = [loader.__class__.__name__ for loader in self.queue]
            handled_destination_tables = self.queued_destination_tables
            print((
                f"\n\033[41mCould not create a queue for the loaders. \033[0m\n"
                f"\033[31mThis issue most likely occured because of circular dependencies. \033[0m\n\n"	
                f"\033[33mUnhappy loaders and their dependencies: \033[0m\033[36m{unhappy_loaders_and_dependencies}. \033[0m\n"
                f"\033[33mHappy loaders: \033[0m\033[36m{happy_loaders}. \033[0m\n"
                f"\033[33mHandled destination tables: \033[0m\033[36m{handled_destination_tables}. \033[0m\n"
            ))
            exit()

        print("\033[32m*** Succesfully created the queue ***\033[0m\n")
        print(self)

    def has_no_unhandled_dependencies(self, loader: DWTableLoader) -> bool:
        # Check if the loader has no unhandled dependencies
        dependencies = loader.insert_dependencies.destination_tables
        for dependency in dependencies:
            if dependency not in self.queued_destination_tables:
                return False
        
        return True

    def perform_load(self):
        # Perform the load
        pass

    def __repr__(self) -> str:
        loader_names_with_index = [f"{i+1}. {loader.__class__.__name__}" for i, loader in enumerate(self.queue)]
        string = "\n    ".join(loader_names_with_index)
        return f"Queue: \n    {string}\n"
