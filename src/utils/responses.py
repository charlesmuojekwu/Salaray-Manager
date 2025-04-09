from fastapi.responses import JSONResponse
from .base_response import SuccessResponse, FailureResponse, PaginatedResponse, PaginationMeta
from typing import Any, List


def success(data: Any = None, message: str = "Success", status_code: int = 200) -> SuccessResponse:
    return SuccessResponse(message=message, data=data, status_code=status_code)


def error(message: str = "An error occurred", status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=FailureResponse(message=message,status_code=status_code).model_dump()
    )


def paginated_response(
    data: List[Any],
    total: int,
    page: int,
    size: int,
    message: str = "Success"
) -> PaginatedResponse:
    pages = (total + size - 1) // size

    return PaginatedResponse(
            status_code=200,
            message=message,
            data=data,
            meta=PaginationMeta(total=total, page=page, size=size, pages=pages)
        )
