from fastapi import FastAPI
from auth.base_config import auth_backend, fastapi_users
from auth.shemas import UserRead, UserCreate
from operation.router import router as router_operation

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)