import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from operation.models import Operation
from operation.schemas import OperationCreate

router = APIRouter(
    prefix='/Operations',
    tags=['Operations']
)


@router.get('/')
async def get_operation(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.execute(query)
        # Получаем список объектов ORM
        orm_objects = result.scalars().all()
        # Преобразовываем каждый объект ORM в словарь
        serializable_results = [obj.as_dict() for obj in orm_objects]
        return {
            'status': 'Успешно',
            'data': serializable_results,
            'details': 'Заебись'
        }
    except Exception as e:
        print(f"Произошла ошибка: {e}")  # Добавляем отладочный вывод
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Пиздец'
        })

@router.post('/')
async def post_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "Добавлено"}


@router.get('/long_operation')
@cache(expire=60)
def get_long_op():
    time.sleep(2)
    return 'Долго'
