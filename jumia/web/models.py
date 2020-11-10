# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    discount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    discounted_price = models.IntegerField(default=0)
    page = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)
