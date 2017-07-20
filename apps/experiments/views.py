# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q

from .models import Experiment

# Create your views here.


class ExpView(View):
    """
    漏洞体验列表功能
    """
    def  get(self,request):
        all_exps = Experiment.objects.all()
        hot_exps = all_exps.order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_exps = all_exps.filter(Q(name__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        sort = request.GET.get('sort', "")

        if sort:
            if sort == "students":
                all_exps = all_exps.order_by("-students")
            elif sort == "hot":
                all_exps = all_exps.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_exps, 3, request=request)
        exps = p.page(page)

        return render(request, 'exps-list.html', {
            "all_exps": exps,
            "sort": sort,
            "hot_exps": hot_exps,
        })