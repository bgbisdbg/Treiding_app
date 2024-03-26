import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from operation.models import operation
from operation.schemas import OperationCreate

router = APIRouter(
    prefix='/Operations',
    tags=['Operations']
)


@router.get('/', response_model=list[OperationCreate])
async def get_operation(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'Успешно',
            'data': result.all(),
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Пиздец'
        })


@router.post('/')
async def post_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "Добавлено"}


@router.get('/long_operation')
@cache(expire=60)
def get_long_op():
    time.sleep(2)
    return 'Долго'
