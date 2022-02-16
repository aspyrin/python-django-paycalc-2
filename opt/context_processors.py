# авторизация, декораторы
from django.contrib.auth.models import User, Group
from django.db.models import Q
# модели
from opt.models import MainMenue

# функция возвращает список пунктов меню для текущего пользователя
def sidebarmenue(request):
    user = request.user # текущий пользователь
    if user.is_authenticated:
        if user.is_superuser:
            return {"menue_list": MainMenue.objects.all()}
        else:
            user_groups = Group.objects.filter(user = request.user) # набор групп пользователя
            menue_list = [] # пустой список для элементов меню
            # перебираем все элементы меню
            for menue_item in MainMenue.objects.all():
                # если пункт для всех групп
                if menue_item.menue_access == "":
                    menue_list.append(menue_item)
                # если установлены разрешения
                else:
                    check = False
                    for ug in user_groups:
                        if ug.name in menue_item.menue_access:
                            check = True
                    if check == True:
                        menue_list.append(menue_item)
            return {"menue_list": menue_list}
    else:
        return {"menue_list": MainMenue.objects.filter(menue_access='')}

# функция выделяет из текущего URL строку адреса для выделения пункта меню
def sidebarmenue_item_selected(request):
    s = '/opt/' # значение по умолчанию
    if request.path.find('/opt/period/', 0, 1000) == 0:
        s = '/opt/period/'
    if request.path.find('/opt/employee/', 0, 1000) == 0:
        s = '/opt/employee/'
    return {"menue_item_selected": s}
