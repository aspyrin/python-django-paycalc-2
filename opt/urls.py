from django.urls import path
from .views import index
from .views import notice_detail
from .views import period_list, period_detail, period_add, period_delete, period_edit
from .views import employee_list, employee_detail, employee_add, employee_delete, employee_edit
from .views import emplcalc_detail

# app_name = 'opt'

urlpatterns = [
    # path('', index),
    path('', index, name='index'),
    path('notice/<int:id>/', notice_detail, name='notice_detail'),

    path('period/', period_list, name='period_list'),
    path('period/add/', period_add, name='period_add'),
    path('period/<int:id>/', period_detail, name='period_detail'),
    path('period/<int:id>/edit/', period_edit, name='period_edit'),
    path('period/<int:id>/delete/', period_delete, name='period_delete'),

    path('employee/', employee_list, name='employee_list'),
    path('employee/add/', employee_add, name='employee_add'),
    path('employee/<int:id>/', employee_detail, name='employee_detail'),
    path('employee/<int:id>/edit/', employee_edit, name='employee_edit'),
    path('employee/<int:id>/delete/', employee_delete, name='employee_delete'),

    path('emplcalc/<int:id>/', emplcalc_detail, name='emplcalc_detail'),
]
