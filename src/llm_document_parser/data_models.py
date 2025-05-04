from typing import List, Literal
from pydantic import BaseModel
from datetime import date

class BankStatementEntry(BaseModel):
    """A single entry in a bank statement."""
    transaction_date: date | None
    description: str | None
    amount: float | None
    transaction_type: Literal['deposit', 'withdrawal', None]

class BankStatement(BaseModel):
    """A bank statement containing multiple transactions."""
    transactions: List[BankStatementEntry] | None
