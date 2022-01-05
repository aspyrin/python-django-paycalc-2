from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .utils import MyUtils


# филиалы
class Branches (models.Model):
    title = models.CharField(max_length=100, blank=False, db_index=True, verbose_name='Название филиала')
    license_num = models.CharField(max_length=10, default='', blank=True, verbose_name='№ лицензия')
    address = models.CharField(max_length=256, default='', blank=True, verbose_name='Адрес')
    phone = models.CharField(max_length=50, default='', blank=True, verbose_name='Телефон')
    app_url = models.CharField(max_length=200, default='#', blank=True, verbose_name='Ссылка на раздел сайта')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Филиалы'    # название модели во множественном числе
        verbose_name = 'Филиал'    # название модели в единственном числе
        ordering = ['title']    # последовательность полей, для сортировки записей


# объявления
class Notice (models.Model):
    title = models.CharField(max_length=256, blank=False, db_index=True, verbose_name='Заголовок')
    content = models.TextField(default='', blank=True, verbose_name='Содержание')
    filial = models.ManyToManyField(
        to='core.Branches', related_name='title_branches',
        blank=False, verbose_name='Филиал'
    )
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    # creator = models.CharField(max_length=50, verbose_name='Опубликовал')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Опубликовал')

    def __str__(self):
        return self.title

    # @property
    def get_filials_str(self):
        str_value = ''
        notice_id = self.pk
        branches = Branches.objects.raw('''SELECT cb.id, cb.title, cb.license_num, cb.address, cb.phone
                                            FROM core_notice_filial cnf
                                            INNER JOIN core_branches cb on cb.id = cnf.branches_id
                                            WHERE cnf.notice_id = %s''', [notice_id])
        for branch in branches:
            str_value += branch.title + '; '
        return str_value
    # get_filials_str.admin_order_field = 'title'
    get_filials_str.boolean = False
    get_filials_str.short_description = 'Филиал'

    def set_creator(self, user):
        self.creator = user


    class Meta:
        verbose_name_plural = 'Объявления'    # название модели во множественном числе
        verbose_name = 'Объявление'    # название модели в единственном числе
        ordering = ['-published']    # последовательность полей, для сортировки записей

    # def save(self, *args, **kwargs):
    #     # self.creator = 1
    #     super().save(*args, **kwargs)