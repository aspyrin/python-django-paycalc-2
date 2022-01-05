from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic import TemplateView    # позволяет использовать базовое представление шаблона

from core.models import Notice
from core.models import Branches
from opt.models import Employee
from opt.models import Position


def index(request):
    branches = Branches.objects.all()
    return render(request, "core/index.html", {'branches': branches})