from django.contrib import admin
from .models import MainMenue
from .models import Position
from .models import PeriodType

# from .models import MotivationRole
# from .models import Employee
# from .models import Period
# from .models import EmployeeCalc
# from .models import BaseModule
# from .models import BaseModuleCalc
# from .models import KpiModule
# from .models import KpiModuleCalc

# последовательность имен полей, выводимых в списке записей
# list_display = ('...', '...', '...', '...')
#
# последовательность имен полей, преобразуемых в гиперссылки, ведущие на страницу правки записей
# list_display_links = ('...', '...')
#
# последовательность имен полей, по которым должна выполняться фильтрация
# search_fields = ('...', '...', '...', '...')
#
# поля, по которым должна выполняться фильтрация
# list_filter = ('...', '...')
#
# последовательность полей, в форме редактора, в кортеже будут в ряд
# fields = ['...', '...', ('...', '...',)]
#
# группировка полей, в форме редактора
# fieldsets = (
#         ('Основные данные', {
#             'fields': ('empl_name','start_date', 'end_date')
#         }),
#         ('Привязки', {
#             'fields': ('status', 'due_back')
#         }),
#         ('Идентификаторы', {
#             'fields': ('inn', 'tab_number', 'login_be', 'id')
#         }),
#     )

# Register your models here.
@admin.register(MainMenue)
class MainMenueAdmin(admin.ModelAdmin):
    list_display = ('menue_sort', 'menue_name', 'menue_parent', 'menue_url', 'menue_access')
    list_display_links = ('menue_name', 'menue_sort')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('pos_name', 'note')
    list_display_links = ('pos_name', 'note')
    # search_fields = ('pos_name', 'note')

@admin.register(PeriodType)
class PeriodTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'note')
    list_display_links = ('type_name', 'note')
    # search_fields = ('pos_name', 'note')

#class KpiModuleInline(admin.StackedInline):
#    model = KpiModule
#    extra = 1
#    fields = ['module_name', 'description', 'creator', 'insertDateTime',]
#    readonly_fields = ('creator', 'insertDateTime',)

#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.set_creator(obj.user)
#        super(KpiModuleInline, self).save_model(request, obj, form, change)

#@admin.register(MotivationRole)
#class MotivationRoleAdmin(admin.ModelAdmin):
#    list_display = ('role_name', 'note',)
#    list_display_links = ('role_name', 'note',)
#    readonly_fields = ('creator', 'insertDateTime',)
#    # search_fields = ('role_name', 'note')
#    fieldsets = [
#        ('Основная информация', {
#            'fields': ['role_name', 'note', 'creator', 'insertDateTime',]
#        }),
#        ('Диапазон заработной платы по роли', {
#            'fields': [('pay_min', 'pay_max')]
#        }),
#        ('Распределение по модулям', {
#            'fields': [('base_percent', 'kpi_percent', 'operation_percent')]
#        }),
#    ]
#    inlines = [BaseModuleInline, KpiModuleInline]

#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.set_creator(obj.user)
#        super(MotivationRoleAdmin, self).save_model(request, obj, form, change)

#@admin.register(BaseModule)
#class BaseModuleAdmin(admin.ModelAdmin):
#    list_display = ('module_name', 'motivationRole')
#    list_display_links = ('module_name', 'motivationRole')
#    fields = ['module_name', 'description', ('use_bossKoeff', 'bossKoeff_min', 'bossKoeff_max'), 'use_ageKoeff', 'use_qualKoeff', 'creator', 'insertDateTime',]
#    readonly_fields = ('creator', 'insertDateTime',)
#    search_fields = ('module_name', 'motivationRole')

#@admin.register(Employee)
#class EmployeeAdmin(admin.ModelAdmin):
#    list_display = ('empl_name', 'inn', 'tab_number', 'start_date', 'end_date', 'motivationRole')
#    list_display_links = ('empl_name', 'inn')
#    search_fields = ('empl_name', 'inn', 'tab_number')
#    list_filter = ('motivationRole', 'end_date')
#    fieldsets = (
#        ('Основные данные', {
#            'fields': ('empl_name','start_date', 'end_date', 'creator', 'insertDateTime',)
#        }),
#        ('Привязки', {
#            'fields': ('position', 'motivationRole')
#        }),
#        ('Идентификаторы', {
#            'fields': ('inn', 'tab_number', 'login_be')
#        }),
#    )
#    readonly_fields = ('creator', 'insertDateTime',)

#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.set_creator(obj.user)
#        super(EmployeeAdmin, self).save_model(request, obj, form, change)



#@admin.register(Period)
#class PeriodAdmin(admin.ModelAdmin):
#    list_display = ('period_type', 'start_date', 'end_date', 'note')
#    list_display_links = ('period_type', 'start_date')
#    fields = ['period_type', 'start_date', 'end_date', 'note', 'creator', 'insertDateTime',]
#    readonly_fields = ('creator', 'insertDateTime',)
#    search_fields = ('period_type', 'start_date', 'end_date', 'note')

#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.set_creator(obj.user)
#        super(PeriodAdmin, self).save_model(request, obj, form, change)

#@admin.register(EmployeeCalc)
#class EmployeeCalcAdmin(admin.ModelAdmin):
#    list_display = ('period', 'employee', 'motivationRole',)
#    list_display_links = ('period', 'employee',)
#    list_filter = ('employee', 'motivationRole',)


# StackedInline - отображение блоком
# TabularInline - отображение в виде таблицы
# class BaseModuleInline(admin.StackedInline):
#    model = BaseModule
#    extra = 1
#    fields = ['module_name', 'description', ('use_bossKoeff', 'bossKoeff_min', 'bossKoeff_max'), 'use_ageKoeff', 'use_qualKoeff', 'creator', 'insertDateTime',]
#    readonly_fields = ('creator', 'insertDateTime',)

#    def save_model(self, request, obj, form, change):
#        obj.user = request.user
#        obj.set_creator(obj.user)
#        super(BaseModuleInline, self).save_model(request, obj, form, change)
