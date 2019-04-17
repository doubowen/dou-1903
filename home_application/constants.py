# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _
from home_application.utils.basic import (choices_to_namedtuple, tuple_choices,
                                  dict_to_choices, tuple_to_namedtuple,
                                  reverse_dict)

########################################################################################################
# PARAMIKO 相关配置
########################################################################################################
RECV_BUFLEN = 32768  # SSH通道recv接收缓冲区大小
RECV_TIMEOUT = 90  # SSH通道recv超时 RECV_TIMEOUT秒
SSH_CON_TIMEOUT = 10  # SSH连接超时设置10s
MAX_WAIT_OUTPUT = 32  # 最大重试等待recv_ready次数
SLEEP_INTERVAL = 0.3  # recv等待间隔

########################################################################################################
# 任务超时控制
########################################################################################################
TASK_TIMEOUT = 600  # 脚本超时控制在600s=10min
JOB_MAX_RETRY = 60  # 默认轮询作业最大次数 100次=3min
JOB_SLEEP_SECOND = 3  # 默认轮询作业周期 3s
MAX_POLL_TIMES = JOB_MAX_RETRY
MAX_UNINSTALL_RETRY = JOB_MAX_RETRY

########################################################################################################
# 第三方系统相关配置
########################################################################################################
# 默认云区域ID
DEFAULT_CLOUD = '0'
# 默认收藏云区域ID列表
DEFAULT_FAVORS = [DEFAULT_CLOUD]
# 作业平台作业成功标志
JOB_SUCCESS = 3

########################################################################################################
# CHOICES
########################################################################################################
AUTH_TUPLE = ('PASSWORD', 'KEY')
AUTH_CHOICES = tuple_choices(AUTH_TUPLE)
AuthType = choices_to_namedtuple(AUTH_CHOICES)

OS_TUPLE = ('WINDOWS', 'LINUX', 'AIX')
OS_CHOICES = tuple_choices(OS_TUPLE)
OsType = choices_to_namedtuple(OS_CHOICES)

NODE_TUPLE = ('AGENT', 'PROXY', 'PAGENT')
NODE_CHOICES = tuple_choices(NODE_TUPLE)
NodeType = choices_to_namedtuple(NODE_CHOICES)

PROC_TUPLE = ('AGENT', 'PLUGIN')
PROC_CHOICES = tuple_choices(PROC_TUPLE)
ProcType = choices_to_namedtuple(PROC_CHOICES)

JOB_TUPLE = (
    'INSTALL_PROXY', 'INSTALL_AGENT', 'INSTALL_PAGENT', 'REINSTALL_PROXY',
    'REINSTALL_AGENT', 'REINSTALL_PAGENT', 'UNINSTALL_AGENT', 'REMOVE_AGENT',
    'UPDATE_PLUGIN', 'UPDATE_CONFIG', 'UPDATE_AUTHINFO', 'UPGRADE_PROXY', 'UPGRADE_AGENT', 'UPGRADE_PAGENT')
JOB_CHOICES = tuple_choices(JOB_TUPLE)
JobType = choices_to_namedtuple(JOB_CHOICES)
JOB_TYPE_DICT = {
    'INSTALL_PROXY': _(u"安装"),
    'INSTALL_AGENT': _(u"安装"),
    'INSTALL_PAGENT': _(u"安装"),
    'REINSTALL_PROXY': _(u"重装"),
    'REINSTALL_AGENT': _(u"重装"),
    'REINSTALL_PAGENT': _(u"重装"),
    'UNINSTALL_AGENT': _(u"卸载"),
    'REMOVE_AGENT': _(u"移除"),
    'UPDATE_PLUGIN': _(u"更新插件"),
    'UPDATE_CONFIG': _(u"更新配置"),
    'UPDATE_AUTHINFO': _(u"更新信息"),
    'UPGRADE_PROXY': _(u"升级"),
    'UPGRADE_AGENT': _(u"升级"),
    'UPGRADE_PAGENT': _(u"升级")
}

OP_TYPE_TUPLE = ('INSTALL', 'REINSTALL', 'UNINSTALL', 'REMOVE', 'UPDATE', 'UPDATE_AUTHINFO', 'UPGRADE')
OP_CHOICES = tuple_choices(OP_TYPE_TUPLE)
OpType = choices_to_namedtuple(OP_CHOICES)

STATUS_TUPLE = ('QUEUE', 'RUNNING', 'SUCCESS', 'FAILED')
STATUS_CHOICES = tuple_choices(STATUS_TUPLE)
StatusType = choices_to_namedtuple(STATUS_CHOICES)

JOB_STATUS_CHOICES = [(0, 'QUEUE',), (1, 'RUNNING',), (2, 'SUCCESS',), (3, 'FAILED',)]
JOB_STATUS_TYPE_DICT = reverse_dict(dict(JOB_STATUS_CHOICES))

LEVEL_TUPLE = ('USER', 'WARNING', 'ERROR')
LEVEL_CHOICES = tuple_choices(LEVEL_TUPLE)
LevelType = choices_to_namedtuple(LEVEL_CHOICES)

CODE_STATUS_TUPLE = (
    "OK", 'UNAUTHORIZED', 'VALIDATE_ERROR', 'METHOD_NOT_ALLOWED',
    'PERMISSION_DENIED', "SERVER_500_ERROR", "OBJECT_NOT_EXIST")
CODE_STATUS_CHOICES = tuple_choices(CODE_STATUS_TUPLE)
ResponseCodeStatus = choices_to_namedtuple(CODE_STATUS_CHOICES)

FLAG_TUPLE = ('STEP', 'EMPTY')
FLAG_CHOICES = tuple_choices(FLAG_TUPLE)
FlagType = choices_to_namedtuple(FLAG_CHOICES)
HEADERS = {
    'Content-type': 'application/json'
}

CODE_TUPLE = (
    # 任务成功
    'INIT',
    'SUCCESS',
    'STILL_RUNNING',
    'CELERY_TASK_EXCEPT',
    'CELERY_TASK_TIMEOUT',
    'WAIT_AGENT_TIMEOUT',
    'UNEXPECTED_RETURN',
    'CURL_FILE_FAILED',
    'REGISTER_FAILED',
    'START_JOB_FAILED',
    'JOB_TIMEOUT',
    'WAIT_AGENT_FAILED',
    'IJOBS_FAILED',
    'FORCE_STOP',
    'INSTALL_FAILED',

    # SSH认证类错误
    'SSH_LOGIN_TIMEOUT', 'SSH_WRONG_PASSWORD',
    'SSH_LOGIN_EXCEPT', 'SSH_LOGIN_KEY_ERR',
    'NOT_SUPPORT_AUTH_WAY', 'SOCKET_TIMEOUT',

    # WMIEXEC
    'UPLOAD_FAILED',
    'DETECT_ARC_FAILED',

    # 其他错误
    'COMMAND_NOT_FOUND',
    'FILE_DOES_NOT_EXIST',
)
CODE_CHOICES = tuple_choices(CODE_TUPLE)
CodeType = choices_to_namedtuple(CODE_CHOICES)

STEP_CHOICES = [
    ('INIT', _(u'任务初始化')),
    ('SSH_LOGIN', _(u'登录目标主机')),
    ('INSTALL_DEP', _(u'安装基础依赖')),
    ('DOWNLOAD_FILE', _(u'下载安装包')),
    ('UPLOAD_FILE', _(u'上传安装包')),
    ('EXECUTE_SCRIPT', _(u'执行安装脚本')),
    ('SCRIPT_DONE', _(u'安装脚本执行完毕')),
    ('REGISTER_CMDB', _(u'注册主机到CMDB')),
    ('WAIT_AGENT', _(u'检测Agent状态和版本')),
    ('CREATE_JOB_SCRIPT', _(u'准备安装脚本')),
    ('CREATE_UNINSTALL_SCRIPT', _(u'准备卸载脚本')),
    ('EXECUTE_JOB', _(u'执行批量安装作业')),
    ('EXECUTE_UNINSTALL_JOB', _(u'执行批量卸载作业')),
    ('DETECT_WIN_ARC', _(u'检测Windows系统版本')),
    ('OVER_SUCCESS', _(u'任务执行成功')),
    ('OVER_FAILED', _(u'任务执行失败')),
]
STEP_DICT = OrderedDict(STEP_CHOICES)
STEP_DISPLAY = {step[0]: step[1] for i, step in enumerate(STEP_CHOICES)}
StepType = tuple_to_namedtuple(STEP_DICT.keys())

PROC_STATE_TUPLE = ('RUNNING', 'UNKNOWN', 'TERMINATED')
PROC_STATE_CHOICES = tuple_choices(PROC_STATE_TUPLE)
ProcStateType = choices_to_namedtuple(PROC_STATE_CHOICES)
PROC_STATUS_DICT = {0: 'UNKNOWN',
                    1: 'RUNNING',
                    2: 'TERMINATED'}


IPROC_STATE_CHOICES = dict_to_choices(PROC_STATUS_DICT)
IPROC_STATUS_DICT = reverse_dict(PROC_STATUS_DICT)

# 安装失败错误码
EXIT_CONDITIONS = (
    'INSTALL_FAILED',
    'SSH_WRONG_PASSWORD',
    'CURL_FILE_FAILED',
    'CELERY_TASK_EXCEPT',
    'UNEXPECTED_RETURN',
)

# 分割信息
JOB_SPLIT = '\n%s\n' % ('#' * 100)
SCRIPT_DICT = {
    OsType.LINUX: 'agent_setup_pro.sh',
    OsType.WINDOWS: 'gse_install.bat',
    OsType.AIX: 'agent_setup_aix.ksh',
}
AIX_PKG_NAME = 'gse_client-aix-powerpc.tgz'

DEFAULT_SCRIPT = 'agent_setup_pro.sh'
