# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import base64
import datetime
import json
import time

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from blueking.component.shortcuts import get_client_by_user
from common.log import logger
from common.mymako import render_json
from home_application.models import OptLog


@task()
def async_task(biz_id, user_name, host_list):
    """
    定义一个 celery 异步任务
    """
    f = open('script/stat.sh')
    s = f.read()
    content = base64.b64encode(s)
    start = time.time()
    client = get_client_by_user(user_name)
    res = client.job.fast_execute_script({
        'bk_biz_id': biz_id,
        'ip_list': host_list,
        'account': 'root',
        'script_type': 1,
        'script_content': content,
        'script_param': '',
    })
    if not res.get('result'):
        return render_json(res)

    task_id = res.get('data').get('job_instance_id')
    while not client.job.get_job_instance_status({
        'bk_biz_id': biz_id,
        'job_instance_id': task_id,
    }).get('data').get('is_finished'):
        print 'waiting job finished...'
        time.sleep(1.2)

    data = client.job.get_job_instance_log({
        'bk_biz_id': biz_id,
        'job_instance_id': task_id
    })
    biz_param = {
        "fields": [
            "bk_biz_name"
        ],
        "condition": {
            "bk_biz_id": int(biz_id)
        },
    }
    action_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    biz_name = client.cc.search_business(biz_param).get('data').get('info')[0].get('bk_biz_name')
    results = data.get('data')[0].get('step_results')
    ip_list = []
    log_list = []
    for result in results:
        for ip_content in result.get("ip_logs"):
            ip = ip_content.get("ip")
            log = ip_content.get('log_content')
            log = ip + "|" + log
            ip_list.append(ip)
            log_list.append(log)
    OptLog.objects.create(
        createUser=user_name,
        log=json.dumps(log_list),
        ipList=json.dumps(ip_list),
        bizID=biz_id,
        bizName=biz_name,
        jobStatus=3,
        actionTime=action_time,
        jobID=int(task_id)
    )













def execute_task(biz_id, user_name, host_list):
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.delay(biz_id, user_name, host_list)


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """

    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))
