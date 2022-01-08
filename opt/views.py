# os
import os
import datetime
# http
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
# авторизация, декораторы
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# механизм уведомления
from django.contrib import messages
# пагинация страниц
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# базовые представления
# from django.views.generic.base import View
# from django.views.generic import TemplateView

# сериализатор наборов запросов to-python Django
from django.core import serializers

# модели данных
from django.contrib.auth.models import User
from django.db.models import Q
from core.models import Notice
from opt.models import Period
from opt.models import PeriodType
from opt.models import Employee
from opt.models import Position
from opt.models import MotivationRole
from opt.models import EmployeeCalc

# формы
from .forms import AddPeriodForm
from .forms import EditPeriodForm
from .forms import EmployeeForm
from .forms import EmployeeFilterForm

# пользовательские классы и функции
from opt.manager import AssemblyEmplCalc
from opt.filters import list_fltr

# декоратор проверки разрешений по группе
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if u.is_superuser or u.groups.filter(name__in=group_names):
                return True
        return False
    return user_passes_test(in_groups)

# домашняя страница в каталоге opt
@login_required
@group_required('buh','opt')
def index(request):

    user = request.user
    title = "Лента новостей филиала"
    annotation = "В данной ленте новостей показан только контент, предназначенный для пользователей сайта ОПТ."
    msg = None

    # получаем значения параметров из строки запроса
    page_param = request.GET.get('page')
    if page_param != 'none':
        cur_page_num = page_param
    else:
        cur_page_num = 1
    notices = Notice.objects.filter(filial__id='1')    # фильтр по Днепр-Опт
    paginator = Paginator(notices, 10)  # 10 строк на каждой странице

    try:
        obj_list_paginated = paginator.page(cur_page_num)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        obj_list_paginated = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        obj_list_paginated = paginator.page(paginator.num_pages)

    # собираем строку фильтра для пагинатора
    # вычисляем количество включенных фильтров
    fltr_str = ""
    fltr_count = 0

    # return render(request, "opt/index.html", {'ntcs': notices})
    return render(request, "opt/index.html", {'ntcs': obj_list_paginated,
                                                # 'fltr_form': fltr_form,
                                                'fltr_str': fltr_str,
                                                'fltr_count': fltr_count,
                                                'title': title,
                                                'annotation': annotation,
                                                'msg': msg})

@login_required
@group_required('buh','opt')
def notice_detail(request, id):
    try:
        # передаем в шаблон данные
        notice_obj = Notice.objects.get(pk=id)
        user = request.user
        title = "Сообщение"
        annotation = "Только для просмотра сотрудниками Опта."
        msg = None

        # обработка пост-запросов
        if request.method == "POST":  # если POST
            # нажатие на кнопку "Закрыть"
            if 'btn_close' in request.POST:
                return redirect('index')

        else:  # если GET
            return render(request, "opt/notice/detail.html", {'notice_obj': notice_obj,
                                                            'title': title,
                                                            'annotation': annotation,
                                                            'msg':msg})
    except Notice.DoesNotExist:
        raise Http404("Сообщение не найдено")

# расчетные периоды
def period_list(request):
    periods = Period.objects.all()
    # periods = Notice.objects.filter(filial__id='1')    # фильтр по Днепр-Опт
    return render(request, "opt/period/list.html", {'period_list': periods})

def period_add(request):
    try:
        period_type_id = request.GET.get("period_type_id", "")
        period_type = PeriodType.objects.get(pk=period_type_id)
        period_obj = Period()
        period_obj.period_type = period_type
        period_obj.creator = request.user
        title = "Добавление нового периода [" + period_obj.period_type.type_name + "]"
        annotation = "Укажите даты начала и окончания периода (обязательно) и примечание (необязательно). Дата окончания не может быть раньше даты начала."
        msg = None
        # обработка пост-запросов
        if request.method == "POST":  # если POST

            # нажатие на кнопку "Добавить"
            if 'btn_add' in request.POST:
                # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
                form = AddPeriodForm(request.POST)
                # Проверка валидности данных формы:
                if form.is_valid():

                    # Прямая выборка неочищенных данных из формы
                    # period_obj.start_date = request.POST.get('inputStartDate')
                    # period_obj.end_date = request.POST.get('inputEndDate')
                    # period_obj.note = request.POST.get('inputNote')
                    # простой вывод результата на страницу (для тестирования)
                    # output = request.POST.get('inputStartDate')
                    # return HttpResponse(output)

                    # проверяем что дата конца не меньше даты начала
                    if form.cleaned_data['end_date'] < form.cleaned_data['start_date']:
                        msg = "Окончание периода не может быть ранее чем Начало периода!"

                    else:
                        # Передаем в модель очищенные данные из form.cleaned_data
                        period_obj.start_date = form.cleaned_data['start_date']
                        period_obj.end_date = form.cleaned_data['end_date']
                        period_obj.note = form.cleaned_data['note']


                        # проверка на дубль периода в БД
                        if period_obj.check_duplicate() == True:
                            msg = "Не может быть создано двух периодов с одинаковыми Типом периода, началом периода и Окончанием периода!"
                        else:
                            # пытаемся добавить объект в БД
                            try:
                                period_obj.save()
                                return redirect('period_list')
                            # ошибка добавления объекта в БД
                            except PeriodType.DoesNotExist:
                                msg = "Период не создан. Неизвестная ошибка"

            # нажатие на кнопку "Отмена"
            if 'btn_cancel' in request.POST:
                return redirect('period_list')

        else:  # если GET
            # определение даты первого дня текущего месяца
            s_date = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
            # определение значений полей формы по умолчанию
            form = AddPeriodForm(initial={'start_date': s_date, 'end_date': datetime.date.today(),})

        return render(request, "opt/period/add.html", {'form': form,
                                                       'period_obj': period_obj,
                                                       'title': title,
                                                       'annotation': annotation,
                                                       'msg':msg})

    except PeriodType.DoesNotExist:
        raise Http404("Неизвестный тип периода")

def period_edit(request, id):
    try:
        # передаем в шаблон данные
        period_obj = Period.objects.get(pk=id)
        emplcalcs = EmployeeCalc.objects.filter(period_id=period_obj.pk)
        user = request.user
        title = "Редактор периода [" + period_obj.period_type.type_name + "]"
        annotation = "Укажите даты начала и окончания периода (обязательно) и примечание (необязательно). Дата окончания не может быть раньше даты начала. Тип периода изменить нельзя."
        msg = None

        # обработка пост-запросов
        if request.method == "POST":  # если POST

            # нажатие на кнопку "Добавить"
            if 'btn_save' in request.POST:
                # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
                form = EditPeriodForm(request.POST)
                # Проверка валидности данных формы:
                if form.is_valid():

                    # Прямая выборка неочищенных данных из формы
                    # period_obj.start_date = request.POST.get('inputStartDate')
                    # period_obj.end_date = request.POST.get('inputEndDate')
                    # period_obj.note = request.POST.get('inputNote')
                    # простой вывод результата на страницу (для тестирования)
                    # output = request.POST.get('inputStartDate')
                    # return HttpResponse(output)

                    # проверяем что дата конца не меньше даты начала
                    if form.cleaned_data['end_date'] < form.cleaned_data['start_date']:
                        msg = "Окончание периода не может быть ранее чем Начало периода!"

                    else:
                        # Передаем в модель очищенные данные из form.cleaned_data
                        period_obj.start_date = form.cleaned_data['start_date']
                        period_obj.end_date = form.cleaned_data['end_date']
                        period_obj.note = form.cleaned_data['note']

                        # пытаемся добавить объект в БД
                        try:
                            period_obj.save()
                            return redirect('period_list')
                        # ошибка добавления объекта в БД
                        except PeriodType.DoesNotExist:
                            msg = "Период не сохранен. Неизвестная ошибка"

            # нажатие на кнопку "Отмена"
            if 'btn_cancel' in request.POST:
                return redirect('period_list')

        else:  # если GET
                form = EditPeriodForm(initial={'start_date': period_obj.start_date,
                                               'end_date': period_obj.end_date,
                                               'note': period_obj.note,})

        return render(request, "opt/period/edit.html", {'period_obj': period_obj,
                                                        'form': form,
                                                        'title': title,
                                                        'annotation': annotation,
                                                        'msg':msg})
    except PeriodType.DoesNotExist:
        raise Http404("Период не найден")

def period_delete(request, id):
    try:
        # передаем в шаблон данные
        period_obj = Period.objects.get(pk=id)
        emplcalcs = EmployeeCalc.objects.filter(period_id=period_obj.pk)
        user = request.user
        title = "Удаление периода [" + period_obj.period_type.type_name + "]"
        msg = None

        # обработка пост-запросов
        if request.method == "POST":  # если POST

            # нажатие на кнопку "Удалить"
            if 'btn_delete' in request.POST:
                period_obj.delete()
                return redirect('period_list')

            # нажатие на кнопку "Отмена"
            if 'btn_cancel' in request.POST:
                return redirect('period_list')

        else:  # если GET
            msg = "Внимание! Будет удален период и все связанные с ним расчеты по сорудникам. Восстановление данных будет невозможно"

        return render(request, "opt/period/delete.html", {'period_obj': period_obj,
                                                          'title': title,
                                                          'msg':msg})

    except PeriodType.DoesNotExist:
        raise Http404("Период не найден")

def period_detail(request, id):
    try:
        # передаем в шаблон данные
        period_obj = Period.objects.get(pk=id)
        emplcalcs = EmployeeCalc.objects.filter(period_id=period_obj.pk)
        user = request.user

        # обработка пост-запросов
        if request.method == "POST":  # если POST
            # нажатие на кнопку "Добавить всех активных"
            if 'createEmplcalcAll' in request.POST:
                period_obj.create_emplcalcs(user)
                return render(request, 'opt/period/detail.html', {'period_obj': period_obj, 'emplcalcs': emplcalcs, })

            # нажатие на кнопку "Добавить всех уволенных"
            elif 'createEmplcalcDisabled' in request.POST:
                # form = NewVenueForm(request.POST)
                # form.fields['title'].required = True
                # form.fields['category'].required = True
                period_obj.create_emplcalcs_disabled(user)
                msg = 'Расчеты по сотрудникам созданы!'
                return render(request, 'opt/period/detail.html', {'period_obj': period_obj, 'emplcalcs': emplcalcs, 'msg': msg,})
                # return HttpResponse("<h2>действие_1</h2>") # редирект

        else:  # если GET
            return render(request, 'opt/period/detail.html', {'period_obj': period_obj, 'emplcalcs': emplcalcs,})

    except Period.DoesNotExist:
        raise Http404("Период не найден")

# расчеты по сотрудникам
def emplcalc_detail(request, id):
    try:
        # передаем в шаблон данные
        emplcalc_obj = EmployeeCalc.objects.get(pk=id)
        log_text_br = emplcalc_obj.note.replace('\n',' <br> ')
        user = request.user
        ecAss = AssemblyEmplCalc(emplcalc_obj)
        # ecAss.build()

        # обработка пост-запросов
        if request.method == "POST":  # если POST
            pass
        else:  # если GET
            return render(request, 'opt/emplcalc/detail.html', {'emplcalc_obj': emplcalc_obj, 'log_text_br': log_text_br, 'ecAssembly': ecAss,})

    except Period.DoesNotExist:
        raise Http404("расчет по сотруднику id=" + str(id) + " не найден")

# сотрудники
@login_required
@group_required('buh')
def employee_list(request):

    user = request.user
    title = "Сотрудники филиала"
    annotation = "Используйте фильтры для быстрого поиска сотрудника. По умолчанию: только активные."
    msg = None

    # получаем значения параметров из строки запроса
    status_param = request.GET.get('status','none')
    name_param = request.GET.get('name','none')
    inn_param = request.GET.get('inn','none')
    tabnum_param = request.GET.get('tabnum','none')
    roleid_param = request.GET.get('roleid','none')
    page_param = request.GET.get('page')
    if page_param != 'none':
        cur_page_num = page_param
    else:
        cur_page_num = 1

    fltr_cons = list() # список с Q-объектами
    if status_param != 'none':
        if status_param == 'active':
            f1 = Q(end_date__isnull = True)
        elif status_param == 'archive':
            f1 = Q(end_date__isnull = False)
        fltr_cons.append(f1)
    if name_param != 'none':
        f2 = Q(empl_name__contains = name_param)
        fltr_cons.append(f2)
    if inn_param != 'none':
        f3 = Q(inn = inn_param)
        fltr_cons.append(f3)
    if tabnum_param != 'none':
        f4 = Q(tab_number = tabnum_param)
        fltr_cons.append(f4)
    if roleid_param != "none":
        try:
           f5 = Q(motivationRole__id = int(roleid_param))
           fltr_cons.append(f5)
        except:
           pass
    fltr_form = EmployeeFilterForm(initial={'status': request.GET.get('status','none'),
                                            'name': request.GET.get('name',''),
                                            'inn': request.GET.get('inn',''),
                                            'tabnum': request.GET.get('tabnum',''),
                                            'roleid': request.GET.get('roleid','none')})
    obj_list_filtered = list_fltr(Employee, fltr_cons)
    paginator = Paginator(obj_list_filtered, 10)  # 10 строк на каждой странице

    try:
        obj_list_paginated = paginator.page(cur_page_num)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        obj_list_paginated = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        obj_list_paginated = paginator.page(paginator.num_pages)

    #собираем строку фильтра для пагинатора
    #вычисляем количество включенных фильтров
    fltr_str = ""
    fltr_count = 0
    if status_param != 'none':
        fltr_str += '&status=' + status_param
        fltr_count = fltr_count + 1
    if name_param != 'none':
        fltr_str += '&name=' + name_param
        fltr_count = fltr_count + 1
    if inn_param != 'none':
        fltr_str += '&inn=' + inn_param
        fltr_count = fltr_count + 1
    if tabnum_param != 'none':
        fltr_str += '&tabnum=' + tabnum_param
        fltr_count = fltr_count + 1
    if roleid_param != "none":
        fltr_str += '&roleid=' + roleid_param
        fltr_count = fltr_count + 1

    return render(request, "opt/employee/list.html", {'employee_list': obj_list_paginated,
                                                    'fltr_form': fltr_form,
                                                    'fltr_str': fltr_str,
                                                    'fltr_count': fltr_count,
                                                    'title': title,
                                                    'annotation': annotation,
                                                    'msg': msg})

@login_required
@group_required('buh')
def employee_detail(request, id):
    try:
        # передаем в шаблон данные
        employee_obj = Employee.objects.get(pk=id)
        user = request.user
        title = "Данные по сотруднику"
        annotation = "Только для просмотра."
        msg = None
        # emplcalcs = employee_obj.empl_calcs.all()

        # обработка пост-запросов
        if request.method == "POST":  # если POST
            # нажатие на кнопку "Закрыть"
            if 'btn_close' in request.POST:
                return redirect('employee_list')

        else:  # если GET
            return render(request, "opt/employee/detail.html", {'employee_obj': employee_obj,
                                                            'title': title,
                                                            'annotation': annotation,
                                                            'msg':msg})
    except Employee.DoesNotExist:
        raise Http404("Сотрудник не найден")

@login_required
@group_required('buh')
def employee_add(request):
    employee_obj = Employee()
    employee_obj.creator = request.user
    title = "Добавление нового сотрудника"
    annotation = "Дата увольнения и примечание не обязательно. Дата увольнения не может быть раньше даты приема."
    msg = None
    # обработка пост-запросов
    if request.method == "POST":  # если POST

        # нажатие на кнопку "Добавить"
        if 'btn_add' in request.POST:
            # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
            form = EmployeeForm(request.POST)

            # Проверка валидности данных формы:
            if form.is_valid():
                # проверка взаимосвязей полей на форме
                if (form.cleaned_data['end_date'] is not None and form.cleaned_data['end_date'] < form.cleaned_data['start_date']):
                    msg = "Дата увольнения не может быть раньше даты приема!"
                else:
                    # Передаем в модель очищенные данные из form
                    employee_obj = form
                    # пытаемся добавить объект в БД
                    try:
                        employee_obj.save()
                        return redirect('employee_list')

                    # ошибка добавления объекта в БД
                    except Employee.DoesNotExist:
                        msg = "Сотрудник не создан. Неизвестная ошибка"

        # нажатие на кнопку "Отмена"
        if 'btn_cancel' in request.POST:
            return redirect('employee_list')

    else:  # если GET
        # определение значений полей формы по умолчанию
        form = EmployeeForm(initial={'start_date': datetime.date.today(),})

    return render(request, "opt/employee/add.html", {'form': form,
                                                       'employee_obj': employee_obj,
                                                       'title': title,
                                                       'annotation': annotation,
                                                       'msg':msg})

@login_required
@group_required('buh')
def employee_delete(request, id):
    try:
        # передаем в шаблон данные
        employee_obj = Employee.objects.get(pk=id)
        user = request.user
        title = "Удаление сотрудника"
        msg = None

        # обработка пост-запросов
        if request.method == "POST":  # если POST

            # нажатие на кнопку "Удалить"
            if 'btn_delete' in request.POST:
                employee_obj.delete()
                return redirect('employee_list')

            # нажатие на кнопку "Отмена"
            if 'btn_cancel' in request.POST:
                return redirect('employee_list')

        else:  # если GET
            msg = "Внимание! Будет удален сотрудник и все связанные с ним расчеты в периодах. Восстановление данных будет невозможно"

        return render(request, "opt/employee/delete.html", {'employee_obj': employee_obj,
                                                          'title': title,
                                                          'msg':msg})

    except Employee.DoesNotExist:
        raise Http404("Сотрудник не найден")

@login_required
@group_required('buh')
def employee_edit(request, id):
    try:
        # передаем в шаблон данные
        employee_obj = Employee.objects.get(pk=id)
        user = request.user
        title = "Редактор сотрудника"
        annotation = "Дата увольнения и примечание не обязательно. Дата увольнения не может быть раньше даты приема."
        msg = None

        # обработка пост-запросов
        if request.method == "POST":  # если POST

            # нажатие на кнопку "Сохранить"
            if 'btn_save' in request.POST:
                # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
                form = EmployeeForm(request.POST, instance=employee_obj)
                # Проверка валидности данных формы:
                if form.is_valid():
                    # проверка взаимосвязей полей на форме
                    if (form.cleaned_data['end_date'] is not None and form.cleaned_data['end_date'] < form.cleaned_data['start_date']):
                        msg = "Дата увольнения не может быть раньше даты приема!"
                    else: # пытаемся добавить объект в БД
                        try:
                            employee_obj.save()
                            return redirect('employee_list')
                        # ошибка добавления объекта в БД
                        except Employee.DoesNotExist:
                            msg = "Сотрудник не сохранен. Неизвестная ошибка"

            # нажатие на кнопку "Отмена"
            if 'btn_cancel' in request.POST:
                return redirect('employee_list')

        else:  # если GET
                form = EmployeeForm(instance=employee_obj)

        return render(request, "opt/employee/edit.html", {'employee_obj': employee_obj,
                                                        'form': form,
                                                        'title': title,
                                                        'annotation': annotation,
                                                        'msg':msg})
    except Employee.DoesNotExist:
        raise Http404("Сотрудник не найден")
