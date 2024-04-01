from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.staticfiles import StaticFiles

from auth.base_config import auth_backend, fastapi_users
from auth.shemas import UserRead, UserCreate
from operation.router import router as router_operation
from tasks.router import router as router_tasks
from redis import ConnectionPool
from pages.router import router as router_pages
from chat.router import router as router_chat


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

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
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)



@app.on_event("startup")
async def startup():
    redis = ConnectionPool.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
