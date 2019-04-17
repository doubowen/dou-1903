# -*- coding: utf-8 -*-
"""
    基础工具包
"""
import os
import re
import stat
import tarfile
import datetime
import paramiko
import posixpath
from collections import Counter, namedtuple

from django.core.exceptions import ValidationError
from django.utils import timezone
from celery.result import AsyncResult

from common.log import logger

# 清理终端颜色
COLOR_REMOVE = re.compile(r'\x1b[^m]*m')
CLEAR_COLOR_RE = re.compile(r'\\u001b\[\D{1}|\[\d{1,2}\D?|\\u001b\[\d{1,2}\D?~?', re.I | re.U)
# 换行转换
LINE_BREAK_RE = re.compile(r'\r\n|\r|\n', re.I | re.U)
# ip地址v4版本
IPV4_RE = re.compile(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}')


def now():
    """
    返回当前时间
    """
    return timezone.now()


def time_delta(hours=1, minutes=30):
    """
    时间间隔
    """
    return datetime.timedelta(hours=hours, minutes=minutes)


def index_of_list(objarr, key, val):
    """
    根据对象的某一属性寻找对象在其所在列表中的位置
    """
    return next((k for k, v in enumerate(objarr) if v[key] == val), -1)


def safe_cast(val, to_type, default=None):
    """
    安全类型转换
    """
    try:
        return to_type(val)
    except ValueError:
        return default or val
    except TypeError:
        return default or val


def duplicate_check(id_list):
    """
    重复元素校验
    """

    # 筛选出现次数大于1的元素
    return len([k for k, v in Counter(id_list).items() if v > 1]) > 0


def safe_remove(file_path):
    """
    安全删除文件
    """
    try:
        os.remove(file_path)
    except:
        pass


def deep_getattr(obj, attr):
    """
    Recurses through an attribute chain to get the ultimate value.
    http://pingfive.typepad.com/blog/2010/04/deep-getattr-python-function.html
    """
    return reduce(getattr, attr.split('.'), obj)


def group_by(item_list, key_or_index_tuple, dict_result=False, aggregate=None, as_key=None):
    """
    对列表中的字典元素进行groupby操作，依据为可排序的某个key
    :param item_list: 待分组字典列表或元组列表
    :param key_or_index_tuple: 分组关键字或位置列表
    :param dict_result: 是否返回字典格式
    :return: 可迭代的groupby对象或者字典
    :ref: http://stackoverflow.com/questions/21674331/group-by-multiple-keys-and-summarize-average-values-of-a-list-of-dictionaries
    """
    from itertools import groupby
    from operator import itemgetter

    list_sorted = sorted(item_list, key=itemgetter(*key_or_index_tuple))
    group_result = groupby(list_sorted, key=itemgetter(*key_or_index_tuple))
    if dict_result:
        return {k: list(g) for k, g in group_result}
    else:
        return group_result


def revoke_task(task):
    """
    递归revoke
    """

    if task.children:
        for child in task.children:
            revoke_task(child)
            # 终止未执行的任务
            # if not task.ready():
            #     task.revoke(terminate=True)

    try:
        task.revoke(terminate=True)
    except:
        pass


def validate_key_data(tag, data):
    """
    密钥(rsa/dsa)内容校验
    """

    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    try:
        tmpfile = StringIO(data)

        if tag == 'rsa':
            paramiko.RSAKey.from_private_key(tmpfile)
            return 'rsa'

        if tag == 'dsa':
            paramiko.DSSKey.from_private_key(tmpfile)
            return 'dsa'

        raise ValidationError('Ssh key type not supported: %s' % tag)
    except paramiko.SSHException as e:
        raise e
    except Exception as e:
        raise e


def validate_key(data):
    """
    先后校验两种密钥文件，不通过则抛异常
    """
    try:
        validate_key_data('rsa', data)
    except paramiko.SSHException:
        validate_key_data('dsa', data)


def parse_color(content):
    """
    成功/失败/正常/异常/结果/返回码
    <span class="agent-color-red">中转机登录失败</span>
    <span class="agent-color-green">192.104.219.102</span>
    <span class="agent-color-gray">192.104.219.102</span>
    <span class="agent-color-black">192.104.219.102</span>
    """

    color_pattern_list = [
        {
            'pattern': [
                u'失败', u'异常', u'超时', u'放弃', u'无法', u'错误码', u'错误', u'批量安装作业启动失败',
                u'command not found', u'error', u'exception', u'timeout', u'failed', u'setup failed',
                u'no such file or directory'
            ],
            'class': 'agent-color-red'
        },
        {
            'pattern': [
                u'执行成功', u'启动成功', u'发送成功', u'成功录入cmdb', u'Done', u'step done',
                u'正常', u'install_success', u'success', u'100%'
            ],
            'class': 'agent-color-green'
        },
        {'pattern': [], 'class': 'agent-color-gray'},
        {
            'pattern': [u'返回码', u'执行完毕', u'作业参数', u'curl',
                        u'status', u'agent状态', u'yum', u'apt-get'],
            'class': 'agent-color-black'
        },
        {'pattern': [
            u'warning', u'执行命令', u'输出结果', u'add crontab task failed. you can add it manually',
            u'register host to cmdb failed. you can add it manually'
        ], 'class': 'agent-color-orange'},
        {'pattern': IPV4_RE, 'class': 'agent-color-black'},
    ]

    # 正则替换
    for color_pattern in color_pattern_list:
        pattern = color_pattern.get('pattern')
        cls = color_pattern.get('class')
        if isinstance(pattern, list):
            # 空规则跳过
            if not pattern:
                continue
            t = re.compile(unicode('|'.join(pattern)), re.IGNORECASE)
        else:
            t = pattern

        pts = set(t.findall(content))
        for kw in pts:
            content = content.replace(kw, u'<span class="{}">{}</span>'.format(cls, kw))
    else:
        return content


def log_parser(content):
    """
    \n\r->换行 + 清理终端颜色码 + 特殊颜色标记
    """
    # content = CLEAR_COLOR_RE.sub('', content)
    content = LINE_BREAK_RE.sub('<br/>', content)
    return content


def strftime_local(aware_time, fmt="%Y-%m-%d %H:%M:%S %z"):
    """格式化aware_time为本地时间"""

    if timezone.is_aware(aware_time):
        return timezone.localtime(aware_time).strftime(fmt)

    return aware_time.strftime(fmt)


def tuple_choices(tupl):
    """从django-model的choices转换到namedtuple"""
    return [(t, t) for t in tupl]


def dict_to_choices(dic, is_reversed=False):
    """从django-model的choices转换到namedtuple"""
    if is_reversed:
        return [(v, k) for k, v in dic.iteritems()]
    return [(k, v) for k, v in dic.iteritems()]


def reverse_dict(dic):
    return {v: k for k, v in dic.iteritems()}


def dict_to_namedtuple(dic):
    """从dict转换到namedtuple"""
    return namedtuple('AttrStore', dic.keys())(**dic)


def choices_to_namedtuple(choices):
    """从django-model的choices转换到namedtuple"""
    return dict_to_namedtuple(dict(choices))


def tuple_to_namedtuple(tupl):
    """从tuple转换到namedtuple"""
    return dict_to_namedtuple(dict(tuple_choices(tupl)))


def revoke_celery_task(task_id):
    """
    终止celery任务
    """

    try:
        task = AsyncResult(task_id)
        task.revoke(terminate=True)
    except Exception as e:
        logger.error(u'revoke_celery_task(Exception): %s' % e)


def rmtree(sftp, remotepath, level=0):
    """
    递归删除操作
    """

    for f in sftp.listdir_attr(remotepath):
        rpath = posixpath.join(remotepath, f.filename)

        # 如果是目录，则递归删除
        if stat.S_ISDIR(f.st_mode):
            rmtree(sftp, rpath, level + 1)
        else:
            sftp.remove(rpath)

    # 删除当前目录
    sftp.rmdir(remotepath)


def ansi_escape(str):
    """终端颜色编码清理"""
    return COLOR_REMOVE.sub('', str)


def extract_tarfile(file_name, target_dir=None):
    """extract tgz file"""
    tar = tarfile.open(file_name)
    target_dir = target_dir or os.path.dirname(file_name)
    tar.extractall(target_dir)
    tar.close()
