# -*- coding: utf-8 -*-
import json

from blueking.component.shortcuts import get_client_by_request, logger
from common.mymako import render_mako_context, render_json
from home_application import celery_tasks
from home_application.biz_utils import get_app_by_user
from home_application.models import OptLog


def home(request):
    """根据用户权限获取业务列表"""
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    # 根据权限查询业务列表
    bk_biz_list = get_app_by_user(request.COOKIES['bk_token'])
    for x in bk_biz_list:
        if x.get("app_name") == u'\u8d44\u6e90\u6c60' or x.get("app_name") == 'Resource pool':
            bk_biz_list.remove(x)
            break

    return render_mako_context(request, '/home_application/home.html', {
        'bk_biz_list': bk_biz_list})


def search_set(request):
    """
    根据业务ID获取集群
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')

    biz_id = request.GET['bizID']
    param = {
        "bk_biz_id": biz_id,
        "fields": [
            "bk_set_name",
            "bk_set_id"
        ]
        }
    res = client.cc.search_set(param)
    set_list = res.get('data').get('info')
    return render_mako_context(request, '/home_application/set_option.html',
                               {'set_list': set_list})


def serch_host(request):
    """
    根据集群获取主机列表
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')

    biz_id = request.GET['bizID']
    set_id = request.GET['setID']
    res = client.cc.search_host({
        "bk_biz_id": biz_id,
        "condition": [
            {
                "bk_obj_id": "set",
                "fields": [],
                "condition": [
                    {
                        "field": "bk_set_id",
                        "operator": "$eq",
                        "value": int(set_id)
                    }
                ]
            }
        ]
    })
    if res.get('result', False):
        bk_host_list = res.get('data').get('info')
    else:
        bk_host_list = []
        logger.error(u"请求主机列表失败：%s" % res.get('message'))
    bk_host_list = [
        {
            'bk_host_name': host['host']['bk_host_name'],
            'bk_host_innerip': host['host']['bk_host_innerip'],
            'bk_cloud_id': host['host']['bk_cloud_id'][0]['bk_inst_id'],
            'bk_cloud_name': host['host']['bk_cloud_id'][0]['bk_inst_name'],
            'bk_os_name': host['host']['bk_os_name']
        }
        for host in bk_host_list
    ]
    return render_mako_context(request, '/home_application/hosts_table.html',
                               {'bk_host_list': bk_host_list})


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def history(request):
    """
    查看历史页面
    """
    client = get_client_by_request(request)
    client.set_bk_api_ver('v2')
    # 根据权限查询业务列表
    bk_biz_list = get_app_by_user(request.COOKIES['bk_token'])
    for x in bk_biz_list:
        if x.get("app_name") == u'\u8d44\u6e90\u6c60' or x.get("app_name") == 'Resource pool':
            bk_biz_list.remove(x)
            break

    return render_mako_context(request, '/home_application/history.html', {
        'bk_biz_list': bk_biz_list})


def search_history(request):
    """
    根据业务id和时间查询历史记录
    :param request:
    :return:
    """
    biz_id = request.GET['bizID']
    if biz_id == 'all':
        history_result = OptLog.objects.all()
    else:
        history_result = OptLog.objects.filter(bizID=biz_id)
    log_list = []
    for history in history_result:
        temp = {
            "createUser": history.createUser,
            "log": history.log,
            "bizName": history.bizName,
            "ipList": history.ipList,
            "actionTime": str(history.actionTime),
            "jobID": history.jobID
        }
        if history.jobStatus == 3:
            temp["jobStatus"] = 'success'
        else:
            temp["jobStatus"] = 'failed'
        log_list.append(temp)
    return render_mako_context(request, '/home_application/history_table.html',
                                   {'log_list': log_list})


def exectue_task(request):
    """
    执行任务
    :param request:
    :return:
    """
    req = json.loads(request.body)
    host_list = req.get('hosts')
    biz_id = req.get('bizID')
    user_name = request.user
    celery_tasks.execute_task(biz_id, user_name, host_list)
    return render_json({
        'result': True,
        'data': '提交成功'})






