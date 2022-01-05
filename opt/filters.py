import os
import datetime
from django.db.models import Q

def list_fltr(model, params = []):
    """ фильтр принимает класс модели и список с Q-объектами, если список пуст, фильтр возвращает все объекты модели все Q-объекты соединены оператором AND """
    param_count = len(params)
    joinQ = Q()
    if param_count == 0:
        queryset = model.objects.all()
    else:
        i = 0
        while i < param_count:
            if i == 0:
                joinQ = params[i]
            else:
                joinQ.add(params[i], Q.AND)
            i += 1
        queryset = model.objects.filter(joinQ)
    return queryset
