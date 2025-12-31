class IRValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, ir):
        for table in ir.tables:
            if table not in self.schema.tables():
                raise ValueError(f"Unknown table: {table}")

        for f in ir.filters:
            table, column = f.column.split(".")
            if column not in self.schema.columns(table):
                raise ValueError(f"Invalid column: {f.column}")

        return True
