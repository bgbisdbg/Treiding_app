from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from operation.router import get_operation

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

temlates = Jinja2Templates(directory='temlates')


@router.get('/base')
def get_base_page(request: Request):
    return temlates.TemplateResponse('base.html', {'request': request})


@router.get('/search/{operation_type}')
def get_search_page(request: Request, operations=Depends(get_operation)):
    return temlates.TemplateResponse('search.html', {'request': request, 'operations': operations['data']})


@router.get('/chat')
def get_chat(request: Request):
    return temlates.TemplateResponse('chat.html', {'request': request})
