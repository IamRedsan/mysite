from enum import Enum

class LoanStatus(Enum):
    MAINTENANCE = "m"
    ON_LOAN = "o"
    AVAILABLE = "a"
    RESERVED = "r"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]

ITEMS_PER_PAGE_BOOKLIST =2

