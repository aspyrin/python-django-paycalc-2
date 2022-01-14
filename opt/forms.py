from django import forms
from django.forms import ModelForm
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
# from django.contrib.admin import widgets

from opt.models import Position
from opt.models import Period
from opt.models import EmployeeCalc
from opt.models import Employee
from opt.models import MotivationRole


class AddPeriodForm(forms.Form):
    start_date = forms.DateField(label='Начало периода', widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='Окончание периода', widget=forms.SelectDateWidget)
    note = forms.CharField(label='Примечание', widget=forms.Textarea, required=False)
    field_order = ["start_date", "end_date", "note"]

class EditPeriodForm(forms.Form):
    start_date = forms.DateField(label='Начало периода', widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='Окончание периода', widget=forms.SelectDateWidget)
    note = forms.CharField(label='Примечание', widget=forms.Textarea, required=False)
    field_order = ["start_date", "end_date", "note"]

class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = ('empl_name',
                  'inn',
                  'login_be',
                  'tab_number',
                  'start_date',
                  'end_date',
                  'note',
                  'position',
                  'motivationRole',)
        widgets = {'empl_name': forms.TextInput(attrs={'class':'txt_field_name'}),
                   'inn': forms.TextInput(attrs={'class':'txt_field_short'}),
                   'login_be': forms.TextInput(attrs={'class':'txt_field_short'}),
                   'tab_number': forms.TextInput(attrs={'class':'txt_field_short'}),
                   'note': forms.Textarea(attrs={'rows': 5, 'class':'form_elem_other'}),
                   'start_date': forms.NumberInput(attrs={'type': 'date', 'class':'txt_field_short'}),
                   'end_date': forms.NumberInput(attrs={'type': 'date', 'class':'txt_field_short'}),
                   'position': forms.Select(attrs={'class':'form_elem_other'}),
                   'motivationRole': forms.Select(attrs={'class':'form_elem_other'}),
                   }
        error_messages = {
            'inn': {'required': _("Это поле обязательно для заполнения."),
                    'unique': _("Такой ИНН уже есть в базе данных. Введите уникальный номер.")
                    }
            }

class EmployeeFilterForm(forms.Form):
    status = forms.ChoiceField(label='Статус', choices=[('active','Активные'), ('archive','Уволенные'),('none','-статус-'),],
                               required=False)
    name = forms.CharField(label='ФИО',
                           required=False,
                           widget=forms.TextInput(attrs={'placeholder': '-Фио-'}))
    inn = forms.CharField(label='ИНН',
                          required=False,
                          widget=forms.TextInput(attrs={'placeholder': '-инн-'}))
    tabnum = forms.CharField(label='Таб.№',
                             required=False,
                             widget=forms.TextInput(attrs={'placeholder': '-таб.№-'}))
    roleid = forms.ChoiceField(label='Мотив.роль',
                               choices=[('none','---мотивационная роль---')] + [(choice.pk, choice.role_name) for choice in MotivationRole.objects.all()],
                               required=False)
    field_order = ['status', 'name', 'inn', 'tabnum', 'roleid']

    status.widget.attrs.update({'class': 'fltr_field_1'})
    name.widget.attrs.update({'class': 'fltr_field_2', })
    inn.widget.attrs.update({'class': 'fltr_field_3'})
    tabnum.widget.attrs.update({'class': 'fltr_field_3'})
    roleid.widget.attrs.update({'class': 'fltr_field_1'})
