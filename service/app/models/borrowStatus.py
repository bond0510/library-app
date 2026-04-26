from enum import Enum

class BorrowStatus(str, Enum):
    ISSUED = "ISSUED"
    OVERDUE = "OVERDUE"
    RETURNED = "RETURNED"