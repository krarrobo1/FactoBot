from typing import TypedDict


class Receipt(TypedDict):
    supplier: str
    expense_type: str
    date: str
    total_amount: float
