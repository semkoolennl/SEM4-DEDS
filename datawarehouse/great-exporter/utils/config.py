BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"

class SourceDatabase:
    def __init__(self, name: str, path: str, type: str):
        self.name = name
        self.path = path
        self.type = type

    def __repr__(self) -> str:
        return (f"{BLUE}SourceDatabase{RESET}:\n"
            f"    {YELLOW}name:              {RESET}{self.name}\n"
            f"    {YELLOW}path:              {RESET}{self.path}\n"
            f"    {YELLOW}type:              {RESET}{self.type}\n"
        )


class SourceCSVDatabase(SourceDatabase):
    def __init__(self, name: str, path: str, delimiter: str, colcount: int):
        super().__init__(name, path, 'csv')
        self.delimiter = delimiter
        self.colcount  = 0

    def __repr__(self) -> str:
        return super().__repr__() + (
            f"    {YELLOW}delimiter:         {RESET}{self.delimiter}\n"
            f"    {YELLOW}hcolcount:         {RESET}{self.colcount}\n"
        )

class SourceSQLite3Database(SourceDatabase):
    def __init__(self, name: str, path: str):
        super().__init__(name, path, 'sqlite3')


class ConnectionConfig:
    def __init__(self, host: str, port: str, database: str, username: str, password: str, driver: str, dialect: str):
        self.host     = host
        self.port     = port
        self.database = database
        self.username = username
        self.password = password
        self.driver   = driver
        self.dialect  = dialect

    def get_sqlalchemy_conn_string(self):
        return f"{self.dialect}://{self.username}:{self.password}@{self.host},{self.port}/{self.database}?driver={self.driver}"
    
    def get_pyodbc_conn_string(self) -> str:
        return (
            f"DRIVER={self.driver};"
            f"SERVER={self.host},{self.port};"
            f"UID={self.username};"
            f"PWD={self.password};"
        )

    def __repr__(self) -> str:
        b = "\033[34m"
        y = "\033[33m"
        r = "\033[0m"
        return (
            f"{b}\nConnectionConfig{r}:\n"
            f"    {y}host:          {r}{self.host}{r}\n"
            f"    {y}port:          {r}{self.port}{r}\n"
            f"    {y}database:      {r}{self.database}{r}\n"
            f"    {y}username:      {r}{self.username}{r}\n"
            f"    {y}password:      {r}{self.password}{r}\n"
            f"    {y}driver:        {r}{self.driver}{r}\n"
            f"    {y}dialect:       {r}{self.dialect}{r}\n"
        )
    
