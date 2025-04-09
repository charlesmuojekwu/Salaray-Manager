
from fastapi import  Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .utils.base_response import  FailureResponse



# Custom exception handler for RequestValidationError
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(loc) for loc in first_error.get("loc", [])) or "unknown"
    message = first_error.get("msg", "Validation error")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": False,
            "message": message,
            "field": field,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        },
    )


# Custom exception handler for HTTPException
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    content = FailureResponse(message=exc.detail, status_code=exc.status_code).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )
    
    
# Generic exception handler for any unexpected errors
async def generic_exception_handler(request: Request, exc: Exception):
    content = FailureResponse(message="An unexpected error occurred", status_code=500).dict()
    return JSONResponse(
        status_code=500,
        content=content
    )