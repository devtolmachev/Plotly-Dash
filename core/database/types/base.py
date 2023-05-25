from core.database.main import Database
from core.database.qmakers import QMaker


class BaseType:
    qm = QMaker()
    database: Database = Database()

    def __init__(self, database: str):
        self.database: Database = Database(database=database)
