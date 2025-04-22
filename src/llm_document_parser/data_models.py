from typing import List, Literal
from pydantic import BaseModel
from datetime import date

class BankStatementEntry(BaseModel):
    transaction_date: date | None
    description: str | None
    amount: float | None
    transaction_type: Literal['deposit', 'withdrawal', None]

class BankStatement(BaseModel):
    transactions: List[BankStatementEntry] | None
