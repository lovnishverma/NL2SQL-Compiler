class IRValidator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, ir):
        # 1. Validate Tables (Pass 1)
        # Ensure every table requested actually exists in the DB
        for table in ir.tables:
            if table not in self.schema.tables():
                raise ValueError(f"Unknown table: {table}")

        # 2. Validate Filter Columns (Pass 2)
        # Ensure columns in WHERE clauses exist and belong to the correct table
        if ir.filters:
            for f in ir.filters:
                self._validate_column_reference(f.column, ir.tables)

        # 3. Validate Metric Columns (Pass 3) - CRITICAL FOR SAFETY
        # This prevents "Hallucinated Aggregations" (e.g., SUM(non_existent_col))
        if ir.metrics:
            for m in ir.metrics:
                self._validate_column_reference(m.column, ir.tables)

        # 4. Validate Dimension Columns (Pass 4)
        # This prevents "Group By Hallucinations"
        if ir.dimensions:
            for d in ir.dimensions:
                self._validate_column_reference(d, ir.tables)

        return True

    def _validate_column_reference(self, column_ref, valid_tables):
        """
        Helper to enforce strict 'table.column' format and schema existence.
        """
        if "." not in column_ref:
            raise ValueError(f"Ambiguous column reference: '{column_ref}'. Must be 'table.column'")
        
        table, col = column_ref.split(".")
        
        # Security Check: Prevent accessing tables not defined in the 'tables' list
        if table not in valid_tables:
            raise ValueError(f"Column '{column_ref}' references table '{table}' which is not in the query scope (tables list).")
        
        # Schema Check: Prevent accessing columns that don't exist in the DB
        schema_columns = self.schema.columns(table)
        if col not in schema_columns:
            raise ValueError(f"Hallucination detected: Column '{col}' does not exist in table '{table}'.")
