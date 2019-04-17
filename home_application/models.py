# -*- coding: utf-8 -*-
from django.db import models


class OptLog(models.Model):
    """操作记录信息"""
    createUser = models.CharField(max_length=100, null=True)
    log = models.CharField(max_length=1000, null=True)
    bizID = models.IntegerField(null=True)
    bizName = models.CharField(max_length=100, null=True)
    ipList = models.CharField(max_length=500, null=True)
    jobStatus = models.IntegerField(null=True)
    actionTime = models.DateTimeField(null=True)
    jobID = models.IntegerField(null=True)

    def toDic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
