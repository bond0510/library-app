from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorCode:
    code: str
    message: str


class ErrorCodes:
    # Borrow domain
    BOOK_NOT_AVAILABLE = ErrorCode(
        code="BORROW_001",
        message="Book not available"
    )

    NO_BORROWS_FOUND = ErrorCode(
        code="BORROW_002",
        message="No borrow records found"
    )

    INVALID_MEMBER = ErrorCode(
        code="BORROW_003",
        message="Invalid member ID"
    )

    # Generic
    INTERNAL_SERVER_ERROR = ErrorCode(
        code="GENERIC_500",
        message="Internal Server Error"
    )

    # Book domain
    INVALID_BOOK_DATA = ErrorCode(
        code="BOOK_001",
        message="Invalid book data")
    
    NO_BOOKS_FOUND = ErrorCode(
        code="BOOK_002", 
        message="No books found")
    
    BOOK_NOT_FOUND = ErrorCode(
        code="BOOK_003", 
        message="Book not found")
    
    BOOK_NOT_AVAILABLE = ErrorCode(
        code="BOOK_004", 
        message= "Book not available")
    
    BOOK_COPY_LIMIT_EXCEEDED = ErrorCode(
        code="BOOK_005",
        message= "Cannot exceed total copies")

    BOOK_ALREADY_EXISTS = ErrorCode(
        code="BOOK_006",
        message="Book with same title and author already exists"
    )

    BOOK_ALREADY_EXISTS = ErrorCode(
        code= "BOOK_001",
         message= "Book already exists"
    )

    #  ADD THIS
    BOOK_ALREADY_ISSUED = ErrorCode(
        code= "BORROW_001",
        message= "Book already issued and not yet returned"
    )

    VALIDATION_ERROR = ErrorCode(
        code="VALIDATION_001",
        message="Validation failed"
    )

    # Member 
    MEMBER_ALREADY_EXISTS = ErrorCode(
        code="MEMBER_001", 
        message="Member already exists")
    
    NO_MEMBERS_FOUND = ErrorCode(
        code="MEMBER_002", 
        message="No members found")
    
    MEMBER_NOT_FOUND = ErrorCode(
        code="MEMBER_003", 
        message="Member not found")