from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date, datetime
from django.utils import timezone

# меню переходов
class MainMenue(models.Model):
    menue_name = models.CharField(max_length=80,
                                blank=False,
                                db_index=True,
                                unique=True,
                                verbose_name='Название',
                                help_text='*обязательное уникальное поле, не более 80 символов')
    menue_sort = models.IntegerField(blank=False,
                                db_index=True,
                                unique=True,
                                verbose_name='Сортировка',
                                help_text='*обязательное уникальное поле, целое число')
    menue_parent = models.IntegerField(blank=True,
                                default=0,
                                db_index=True,
                                unique=False,
                                verbose_name='Родительский элемент',
                                help_text='*необязательное поле, целое число')
    menue_url = models.CharField(max_length=256,
                                blank=False,
                                verbose_name='Ссылка на страницу',
                                help_text='*обязательное поле, не более 256 символов')
    menue_icon = models.CharField(max_length=256,
                                blank=True,
                                verbose_name='Ссылка на иконку',
                                help_text='*необязательное поле, не более 256 символов')
    menue_help = models.CharField(max_length=256,
                                blank=True,
                                verbose_name='Вспомогательный текст',
                                help_text='*необязательное поле, не более 256 символов')
    menue_access = models.CharField(max_length=256,
                                blank=True,
                                verbose_name='Кортеж с группами доступа (разрешения)',
                                help_text='*необязательное поле, не более 256 символов')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return self.menue_name

    def set_creator(self, user):
        self.creator = user

    class Meta:
        verbose_name_plural = 'Пункты меню'  # название модели во множественном числе
        verbose_name = 'Пункт меню'  # название модели в единственном числе
        ordering = ['menue_sort']  # последовательность полей, для сортировки записей

# мотивационные роли
class MotivationRole(models.Model):
    role_name = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Название роли')
    pay_max = models.FloatField(default=0, verbose_name='Макс. ЗП с налогами, грн')
    pay_min = models.FloatField(default=0, verbose_name='Мин. ЗП с налогами, грн')
    base_percent = models.FloatField(default=100, verbose_name='Доля окладной части, %')
    kpi_percent = models.FloatField(default=0, verbose_name='Доля KPI части, %')
    operation_percent = models.FloatField(default=0, verbose_name='Доля сдельной части, %')
    note = models.TextField(default='', blank=True, verbose_name='Описание')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return self.role_name

    def get_absolute_url(self):
        return f'/opt/motivationrole/{self.pk}/'

    def set_creator(self, user):
        self.creator = user

    # функции получения модулей
    def get_base_module(self):
        obj = BaseModule.objects.get(motivationRole=self)
        return obj

    def get_kpi_module(self):
        obj = KpiModule.objects.get(motivationRole=self)
        return obj

    def get_piecework_module(self):
        pass

    def get_dotation_module(self):
        pass

    def get_premium_module(self):
        pass

    def get_surcharge_module(self):
        pass

    def get_mulct_module(self):
        pass

    class Meta:
        verbose_name_plural = 'Мотивационные роли'  # название модели во множественном числе
        verbose_name = 'Мотивационная роль'  # название модели в единственном числе
        ordering = ['role_name']  # последовательность полей, для сортировки записей

# должность по штатному расписанию
class Position(models.Model):
    pos_name = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Должность по ШР')
    note = models.TextField(default='', blank=True, verbose_name='Примечание')

    def __str__(self):
        return self.pos_name

    def get_absolute_url(self):
        return f'/opt/position/{self.pk}/'

    class Meta:
        verbose_name_plural = 'Должности по ШР'  # название модели во множественном числе
        verbose_name = 'Должность по ШР'  # название модели в единственном числе
        ordering = ['pos_name']  # последовательность полей, для сортировки записей

# сотрудник
class Employee(models.Model):
    empl_name = models.CharField(max_length=100,
                                 blank=False,
                                 db_index=True,
                                 unique=True,
                                 verbose_name='ФИО',
                                 help_text='*обязательное уникальное поле, не более 100 символов')
    inn = models.CharField(max_length=10,
                           blank=False,
                           db_index=True,
                           unique=True,
                           verbose_name='ИНН',
                           help_text='*обязательное уникальное поле, не более 20 символов')
    login_be = models.CharField(max_length=15,
                                default='',
                                blank=True,
                                db_index=True,
                                verbose_name='Логин ВЕ')
    tab_number = models.CharField(max_length=10,
                                  blank=False,
                                  db_index=True,
                                  unique=True,
                                  verbose_name='Таб номер',
                                  help_text='*обязательное уникальное поле, не более 10 символов')
    start_date = models.DateField(db_index=True,
                                  blank=False,
                                  verbose_name='Принят',
                                  help_text='*обязательное поле')
    end_date = models.DateField(db_index=True,
                                null=True,
                                blank=True,
                                verbose_name='Уволен')
    note = models.TextField(default='',
                            blank=True,
                            verbose_name='Примечание')
    position = models.ForeignKey(Position,
                                 on_delete=models.PROTECT,
                                 related_name='employees',
                                 null=True,
                                 db_index=True,
                                 blank=False,
                                 verbose_name='Должность по ШР',
                                 help_text='*обязательное поле')
    motivationRole = models.ForeignKey(MotivationRole,
                                       on_delete=models.PROTECT,
                                       related_name='employees',
                                       null=True,
                                       db_index=True,
                                       blank=False,
                                       verbose_name='Мотивационная роль',
                                       help_text='*обязательное поле')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return self.empl_name

    def get_absolute_url(self):
        return f'/opt/employee/{self.pk}/'

    def set_creator(self, user):
        self.creator = user

    # функция проверки уникальности кодов
    def check_inn(self):
        if not Employee.objects.filter(inn=self.inn).exists():
            return False
        else:
            return True

    def check_login_be(self):
        if not Employee.objects.filter(login_be=self.login_be).exists():
            return False
        else:
            return True

    def check_tab_number(self):
        if not Employee.objects.filter(tab_number=self.tab_number).exists():
            return False
        else:
            return True

    class Meta:
        verbose_name_plural = 'Сотрудники'  # название модели во множественном числе
        verbose_name = 'Сотрудник'  # название модели в единственном числе
        ordering = ['empl_name']  # последовательность полей, для сортировки записей

# тип расчетного периода
class PeriodType(models.Model):
    type_name = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Название типа')
    note = models.TextField(default='', blank=True, verbose_name='Примечание')

    def __str__(self):
        return self.type_name

    def get_absolute_url(self):
        return f'/opt/periodtype/{self.pk}/'

    class Meta:
        verbose_name_plural = 'Типы периодов'  # название модели во множественном числе
        verbose_name = 'Тип периода'  # название модели в единственном числе
        ordering = ['type_name']  # последовательность полей, для сортировки записей

# расчетный период
class Period(models.Model):
    # period_name = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Имя')
    period_type = models.ForeignKey(PeriodType,
                                    on_delete=models.PROTECT,
                                    related_name='periods',
                                    null=False,
                                    default=1,
                                    db_index=True,
                                    blank=False,
                                    verbose_name='Тип периода')
    start_date = models.DateField(db_index=True, blank=False, verbose_name='Начало периода')
    end_date = models.DateField(db_index=True, null=True, blank=True, verbose_name='Окончание периода')
    note = models.TextField(default='', blank=True, verbose_name='Примечание')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=1, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return str(self.start_date) + ' - ' + str(self.end_date) + ' [' + str(self.period_type) + ']'

    def get_absolute_url(self):
        # return reverse('myurl', kwargs={'id': self.id, 'name': self.period_name})
        return f'/opt/period/{self.pk}/'

    # функция проверки аналогичного периода
    def check_duplicate(self):
        if not Period.objects.filter(period_type=self.period_type, start_date=self.start_date, end_date=self.end_date).exists():
            return False
        else:
            return True

    # создание расчетов по сотрудникам и сохранение в базе
    def create_emplcalcs(self, user):
        cur_empl_list = Employee.objects.filter(end_date=None)
        for empl_obj in cur_empl_list:
            create_emplcalc(empl_obj, user)
        #    empl_calc = EmployeeCalc(employee=empl_obj,
        #                             period=self,
        #                             note='Расчет создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n')
        #    empl_calc.save()

    # создание расчетов по уволенным сотрудникам в данном периоде
    def create_emplcalcs_disabled(self, user):
        pYear = self.start_date.year
        pMonth = self.start_date.month
        # cur_empl_list = Employee.objects.filter(end_date__range=["2011-01-01", "2011-01-31"])
        cur_empl_list = Employee.objects.filter(end_date__year=pYear, end_date__month=pMonth)
        for empl_obj in cur_empl_list:
            self.create_emplcalc(empl_obj, user)
        #    empl_calc = EmployeeCalc(employee=empl_obj,
        #                             period=self,
        #                             motivationRole=empl_obj.motivationRole,
        #                             note='Расчет создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n')
        #    empl_calc.save()
        #    empl_calc.build_modules(user)

    # создание расчета по сотруднику в данном периоде
    def create_emplcalc(self, employee, user):
            empl_calc = EmployeeCalc(employee=employee,
                                     period=self,
                                     motivationRole=employee.motivationRole,
                                     note='Расчет создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n')
            empl_calc.save()
            empl_calc.build_modules(user)

    # получить список расчетов по сотрудникам в виде строки
    # @property
    def get_emplcalcs_str(self):
        str_value = ''
        period_id = self.pk
        emplcalcs = EmployeeCalc.objects.raw('''SELECT emplclc.id, emplclc.employee_id, emplclc.period_id, emplclc.note
                                            FROM opt_employeecalc emplclc
                                            INNER JOIN opt_employee empl on empl.id = emplclc.employee_id
                                            WHERE emplclc.period_id = %s''', [period_id])
        for emplclc in emplcalcs:
            str_value += str(emplclc.id) + '; '
        return str_value

    # get_emplcalcs_str.admin_order_field = 'empl_name'
    # get_emplcalcs_str.boolean = False
    # get_emplcalcs_str.short_description = 'Расчеты по сотрудникам за период'

    # получить список расчетов по сотрудникам в виде списка
    # @property
    def get_emplcalcs_list(self):
        emplcalcs = EmployeeCalc.objects.filter(period_id=self.pk)
        return emplcalcs

    class Meta:
        unique_together = ('period_type', 'start_date', 'end_date')
        verbose_name_plural = 'Расчетные периоды'  # название модели во множественном числе
        verbose_name = 'Расчетный период'  # название модели в единственном числе
        ordering = ['-start_date', 'period_type']  # последовательность полей, для сортировки записей

# расчетный период по сотруднику
class EmployeeCalc(models.Model):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 related_name='empl_calcs',
                                 null=False,
                                 db_index=True,
                                 blank=False,
                                 verbose_name='Сотрудник')
    period = models.ForeignKey(Period,
                               on_delete=models.CASCADE,
                               related_name='empl_calcs',
                               null=False,
                               db_index=True,
                               blank=False,
                               verbose_name='Период')
    motivationRole = models.ForeignKey(MotivationRole,
                                       on_delete=models.PROTECT,
                                       related_name='empl_calcs',
                                       null=True,
                                       db_index=True,
                                       blank=True,
                                       verbose_name='Мотивационная роль')
    note = models.TextField(default='', blank=True, verbose_name='Лог расчета')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return str(self.employee) + ' - [' + str(self.period) + ']'

    def get_absolute_url(self):
        # return reverse('myurl', kwargs={'id': self.id, 'name': self.period_name})
        return f'/opt/emplcalc/{self.pk}/'


    def get_base_module_calc(self):
        bmc = BaseModuleCalc.objects.get(employee_calc=self)
        return bmc

    def get_kpi_module_calc(self):
        kpimc = KpiModuleCalc.objects.get(employee_calc=self)
        return kpimc

    def get_piecework_module_calc(self):
        pass

    # собрать все модули расчета по сотруднику
    def build_modules(self, user):
        # сборка расчета по базовому модулю
        base_module = self.motivationRole.get_base_module()
        base_module_calc = BaseModuleCalc(parent_module=base_module,
                                          employee_calc=self,
                                          calc_log='Модуль создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n')
        base_module_calc.save()
        self.note += 'Базовый модуль создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n'

        # сборка расчета по KPI модулю
        kpi_module = self.motivationRole.get_kpi_module()
        kpi_module_calc = KpiModuleCalc(parent_module=kpi_module,
                                          employee_calc=self,
                                          calc_log='Модуль создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n')
        kpi_module_calc.save()
        self.note += 'KPI модуль создан - ' + str(datetime.now()) + '(' + str(user) + ')' + '\n'

        # сохранить расчет по сотруднику
        self.save()

    class Meta:
        unique_together = ('employee', 'period')
        verbose_name_plural = 'Расчеты по сотрудникам'  # название модели во множественном числе
        verbose_name = 'Расчет по сотруднику'  # название модели в единственном числе
        ordering = ['period', 'employee']  # последовательность полей, для сортировки записей

# базовый модуль
class BaseModule(models.Model):
    module_name = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Название')
    description = models.TextField(
        default='Расчет по базовому модулю = (Исх. знач. окладной части / Норма часов / Факт часов) * К рук. * К стаж. * К квал.',
        blank=True, verbose_name='Описание')
    motivationRole = models.OneToOneField(MotivationRole,
                                          on_delete=models.CASCADE,
                                          related_name='base_modules',
                                          null=True, db_index=True,
                                          blank=False,
                                          verbose_name='Мотивационная роль')
    use_bossKoeff = models.BooleanField(default=True, verbose_name='Использовать коэффициент руководитея')
    bossKoeff_max = models.FloatField(default=1, verbose_name='Максимальное значение коэффициент руководитея')
    bossKoeff_min = models.FloatField(default=1, verbose_name='Минимальное значение коэффициент руководитея')
    use_ageKoeff = models.BooleanField(default=True, verbose_name='Использовать коэффициент стажа')
    use_qualKoeff = models.BooleanField(default=True, verbose_name='Использовать коэффициент квалификации')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return self.module_name

    def get_absolute_url(self):
        return f'/opt/basemodule/{self.pk}/'

    def set_creator(self, user):
        self.creator = user

    class Meta:
        verbose_name_plural = 'Базовые модули'  # название модели во множественном числе
        verbose_name = 'Базовый модуль'  # название модели в единственном числе
        ordering = ['module_name']  # последовательность полей, для сортировки записей

# расчет базового модуля
class BaseModuleCalc(models.Model):
    parent_module = models.ForeignKey(BaseModule,
                                      on_delete=models.CASCADE,
                                      related_name='base_module_calcs',
                                      null=False,
                                      db_index=True,
                                      blank=False,
                                      verbose_name='Родительский модуль')
    employee_calc = models.ForeignKey(EmployeeCalc,
                                      on_delete=models.CASCADE,
                                      related_name='base_module_calcs',
                                      null=False,
                                      db_index=True,
                                      blank=False,
                                      verbose_name='Расчет по сотруднику за период')
    inputValue = models.FloatField(null=True, blank=True, default=0,
                                   verbose_name='Исходное значение окладной части')
    bossKoeff_fact = models.FloatField(null=True, blank=True, default=1,
                                       verbose_name='Фактическое значение коэффициент руководитея')
    ageKoeff_fact = models.FloatField(null=True, blank=True, default=1,
                                      verbose_name='Фактическое значение коэффициента стажа')
    qualKoeff_fact = models.FloatField(null=True, blank=True, default=1,
                                       verbose_name='Фактическое значение коэффициента квалификации')
    outValue_saved = models.FloatField(null=True, blank=True, default=0,
                                       verbose_name='ИТОГО ПО ОКЛАДНОЙ ЧАСТИ (Сохранено)')
    calc_log = models.TextField(default='', blank=True,
                                verbose_name='Лог расчета')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return '[' + str(self.parent_module) + ']-[' + str(self.employee_calc) + ']'

    def get_absolute_url(self):
        return f'/opt/basemodulecalc/{self.pk}/'

    class Meta:
        verbose_name_plural = 'Расчеты по базовым модулям'  # название модели во множественном числе
        verbose_name = 'Расчет по базовому модулю'  # название модели в единственном числе

# KPI модуль
class KpiModule(models.Model):
    module_name = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Название')
    description = models.TextField(
        default='Расчет по KPI модулю = (Исх. знач. переменной части * К эфф.)',
        blank=True, verbose_name='Описание')
    motivationRole = models.OneToOneField(MotivationRole,
                                          on_delete=models.CASCADE,
                                          related_name='kpi_modules',
                                          null=True, db_index=True,
                                          blank=False,
                                          verbose_name='Мотивационная роль')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return self.module_name

    def get_absolute_url(self):
        return f'/opt/kpimodule/{self.pk}/'

    def set_creator(self, user):
        self.creator = user


    class Meta:
        verbose_name_plural = 'KPI модули'  # название модели во множественном числе
        verbose_name = 'KPI модуль'  # название модели в единственном числе
        ordering = ['module_name']  # последовательность полей, для сортировки записей

# расчет KPI модуля
class KpiModuleCalc(models.Model):
    parent_module = models.ForeignKey(KpiModule,
                                      on_delete=models.CASCADE,
                                      related_name='kpi_module_calcs',
                                      null=False,
                                      db_index=True,
                                      blank=False,
                                      verbose_name='Родительский модуль')
    employee_calc = models.ForeignKey(EmployeeCalc,
                                      on_delete=models.CASCADE,
                                      related_name='kpi_module_calcs',
                                      null=False,
                                      db_index=True,
                                      blank=False,
                                      verbose_name='Расчет по сотруднику за период')
    inputValue = models.FloatField(null=True, blank=True, default=0,
                                   verbose_name='Исходное значение переменной части')
    outValue_saved = models.FloatField(null=True, blank=True, default=0,
                                       verbose_name='ИТОГО ПО KPI МОДУЛЮ (Сохранено)')
    calc_log = models.TextField(default='', blank=True,
                                verbose_name='Лог расчета')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=False, default=4, verbose_name='Создатель')
    insertDateTime = models.DateTimeField(default=timezone.now, null=False, verbose_name='Создано')

    def __str__(self):
        return '[' + str(self.parent_module) + ']-[' + str(self.employee_calc) + ']'

    def get_absolute_url(self):
        return f'/opt/kpimodulecalc/{self.pk}/'

    class Meta:
        verbose_name_plural = 'Расчеты по KPI модулям'  # название модели во множественном числе
        verbose_name = 'Расчет по KPI модулю'  # название модели в единственном числе
