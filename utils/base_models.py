# -*- coding: utf-8 -*-

from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    # is_delete = models.SmallIntegerField('删除状态', default=1, help_text='删除状态')

    class Meta:
        # 指定在迁移时不创建表
        abstract = True

