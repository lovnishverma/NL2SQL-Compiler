from typing import List, Optional
from pydantic import BaseModel, Field


class Metric(BaseModel):
    column: str
    operation: str = Field(
        description="SUM | COUNT | AVG | MIN | MAX"
    )


class Filter(BaseModel):
    column: str
    operator: str = Field(
        description="= | != | > | < | >= | <="
    )
    value: str


class Join(BaseModel):
    left_table: str
    right_table: str
    left_column: str
    right_column: str


class QueryIR(BaseModel):
    intent: str = Field(
        description="select | aggregation"
    )
    tables: List[str]
    metrics: Optional[List[Metric]] = []
    dimensions: Optional[List[str]] = []
    filters: Optional[List[Filter]] = []
    joins: Optional[List[Join]] = []
