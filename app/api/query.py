from fastapi import APIRouter, HTTPException
from app.core.ir import QueryIR
from app.core.schema import DatabaseSchema
from app.core.validator import IRValidator
from app.core.compiler import SQLCompiler

router = APIRouter()

# SQLite for now (stable, portable)
DB_URL = "sqlite:///examples/db.sqlite"

schema = DatabaseSchema(DB_URL)
validator = IRValidator(schema)
compiler = SQLCompiler()


@router.post("/query")
def query(ir: QueryIR):
    try:
        validator.validate(ir)
        sql = compiler.compile(ir)
        return {
            "sql": sql,
            "explanation": "SQL generated from validated semantic IR"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
