from sqlalchemy import create_engine, inspect


class DatabaseSchema:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.inspector = inspect(self.engine)

    def tables(self):
        return self.inspector.get_table_names()

    def columns(self, table: str):
        return {
            col["name"]: col["type"]
            for col in self.inspector.get_columns(table)
        }

    def foreign_keys(self, table: str):
        return self.inspector.get_foreign_keys(table)
