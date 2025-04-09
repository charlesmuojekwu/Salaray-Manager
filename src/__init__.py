# from fastapi import FastAPI,HTTPException
# from fastapi.exceptions import RequestValidationError
# from fastapi.middleware.cors import CORSMiddleware
# from contextlib import asynccontextmanager
# from .exception_handlers import custom_http_exception_handler, generic_exception_handler, validation_exception_handler
# from src.employee.routers import employee_router
# from src.employee_agreement.routers import employee_agreement_router
# from src.auth.routers import auth_router

# from src.db.main import init_db


# @asynccontextmanager
# async def life_span(app:FastAPI):
#     print(f"server is started")
#     await init_db()
#     yield
#     print(f"server has been stopped....")
    

# version = "v1"

# app = FastAPI(
#     title="Salary Tracker",
#     description="Salary and task management application",
#     version = version,
#     lifespan=life_span
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.add_exception_handler(HTTPException, custom_http_exception_handler)
# app.add_exception_handler(Exception, generic_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)


# app.include_router(employee_router, prefix=f"/api/{version}/employee", tags=['employee'])
# app.include_router(employee_agreement_router, prefix=f"/api/{version}/agreement", tags=['agreement'])
# app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])