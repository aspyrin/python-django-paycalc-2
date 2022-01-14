from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .utils import MyUtils
# пакеты для работы с файлами
from django.core.validators import FileExtensionValidator
import uuid
from pathlib import Path


# функция возвращает путь к файлу (MEDIA_ROOT/<model_name>/<file_name>) с расширением
def documents_directory_path(instance, filename):
    new_dir_name = str(instance.__class__.__name__).lower()
    file_extension = Path(filename).suffix[1:].lower()
    new_file_name = 'notice_id_' + str(instance.notice.id) + '_file_id_' + str(instance.unique_id) + '.' + file_extension
    return '{0}/{1}'.format(new_dir_name, new_file_name)

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


# вложения в объявления
class NoticiesDocs (models.Model):
    first_name = models.CharField(max_length=500,
                                    blank=False,
                                    default='unknown_file',
                                    db_index=True,
                                    verbose_name='Исходное имя файла')
    notice = models.ForeignKey(Notice,
                                on_delete=models.PROTECT,
                                related_name='documents',
                                null=True,
                                db_index=True,
                                blank=False,
                                verbose_name='Сообщение',
                                help_text='*обязательное поле, максимально 500 символов')
    document = models.FileField(upload_to=documents_directory_path,
                                max_length=500,
                                validators=[FileExtensionValidator(allowed_extensions=('pdf', 'doc', 'docx', 'xls', 'xlsx', 'xlsm','jpg', 'png',))],
                                verbose_name='Ссылка',)
    published = models.DateTimeField(auto_now_add=True,
                                        db_index=True,
                                        verbose_name='Опубликовано')
    creator = models.ForeignKey(User, on_delete=models.PROTECT,
                                verbose_name='Опубликовал')
    unique_id = models.CharField(max_length=100,
                                    blank=True,
                                    unique=True,
                                    default=uuid.uuid4,
                                    editable=False)

    def __str__(self):
        # return self.document.name
        return self.first_name

    def set_creator(self, user):
        self.creator = user

    # функция удаляет старый файл при загрузке нового файла в модели
    def remove_on_document_update(self):
        try:
            # is the object in the database yet?
            obj = NoticiesDocs.objects.get(id=self.id)
        except NoticiesDocs.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.document and self.document and obj.document != self.document:
            # delete the old image file from the storage in favor of the new file
            obj.document.delete()

    # функция удаляет файл при удалении модели из БД
    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.document.delete()
        return super(NoticiesDocs, self).delete(*args, **kwargs)

    # запуск функци проверки/удаления файла на событие save
    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_document_update()
        return super(NoticiesDocs, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Документы'    # название модели во множественном числе
        verbose_name = 'Документ'    # название модели в единственном числе
        ordering = ['notice', '-published']    # последовательность полей, для сортировки записей
