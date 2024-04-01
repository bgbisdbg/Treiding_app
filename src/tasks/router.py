from typing import Any

from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from auth.base_config import current_user
from tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix='/report')


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    # bacgraunt.add_task(send_email_report_dashboard, user.username) - с использование отложенной задачи самого fastapi (Так же нужно первым аргументом передать (bacgraunt: BackgroundTask))
    # send_email_report_dashboard(user.username) - просто отправка почты
    send_email_report_dashboard.delay(user.username)
    return {
        'status': 200,
        'data': 'Письмо отпарвлено',
        'details': None
    }
