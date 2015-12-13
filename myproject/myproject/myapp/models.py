# -*- coding: utf-8 -*-
from django.db import models

import customStorage

fs = customStorage.MyStorage()

class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(upload_to='media', storage=fs)
