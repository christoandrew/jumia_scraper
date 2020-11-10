# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from models import Product


def index(request):
    products = Product.objects.filter(name__isnull=False).order_by("discounted_price")
    return render(request, "web/index.html", context={"products": products})
