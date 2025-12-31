class SQLCompiler:
    def compile(self, ir):
        select_parts = []

        if ir.metrics:
            for m in ir.metrics:
                select_parts.append(
                    f"{m.operation}({m.column})"
                )
        else:
            select_parts.append("*")

        select_clause = "SELECT " + ", ".join(select_parts)
        from_clause = "FROM " + ", ".join(ir.tables)

        where_clause = ""
        if ir.filters:
            conditions = [
                f"{f.column} {f.operator} '{f.value}'"
                for f in ir.filters
            ]
            where_clause = "WHERE " + " AND ".join(conditions)

        group_by_clause = ""
        if ir.dimensions:
            group_by_clause = "GROUP BY " + ", ".join(ir.dimensions)

        return " ".join(
            [select_clause, from_clause, where_clause, group_by_clause]
        ).strip()
