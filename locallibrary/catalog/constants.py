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
ITEMS_PER_PAGE_COPIES =2
ITEMS_PER_PAGE_LOANBOOKS =2
AUTHORS_PER_PAGE=2
DEFAULT_DATE_OF_DEATH = "01/01/2099"

