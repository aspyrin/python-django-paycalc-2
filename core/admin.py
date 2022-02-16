from django.contrib import admin
from django.contrib.auth.models import User
from pathlib import Path
# пользовательские глобальные функции
from utils.global_func import get_image_name_by_ext
# модели
from .models import Branches
from .models import Notice
from .models import NoticiesDocs


@admin.register(Branches)
class BranchesAdmin(admin.ModelAdmin):
    list_display = ('title', 'license_num', 'address', 'phone')
    list_display_links = ('title',)


# @admin.register(NoticiesDocs)
class NoticiesDocsInline(admin.TabularInline):
    model = NoticiesDocs
    extra = 0
    fields = ['document', 'creator', 'published',]
    readonly_fields = ('document', 'creator', 'published',)

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #    return False


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published', 'creator', 'get_filials_str', 'get_doc_count',)
    list_display_links = ('title',)
    search_fields = ('title', 'content',)
    readonly_fields = ('creator', 'published',)
    fields = ['title', 'content', 'filial', 'published', 'creator',]
    inlines = [NoticiesDocsInline,]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.set_creator(obj.user)
        super(NoticeAdmin, self).save_model(request, obj, form, change)


@admin.register(NoticiesDocs)
class NoticiesDocsAdmin(admin.ModelAdmin):
    list_display = ('notice', 'first_name', 'document', 'published', 'creator', )
    list_display_links = ('first_name',)
    readonly_fields = ('first_name', 'published', 'creator', 'ext_ico', 'ext_name')
    list_filter = ('notice',)
    # search_fields = ('notice',)

    def save_model(self, request, obj, form, change):
        obj.set_creator(request.user)
        obj.first_name = obj.document.name
        obj.ext_name = Path(obj.document.name).suffix[1:].lower()
        obj.ext_ico = get_image_name_by_ext(obj.ext_name)
        super(NoticiesDocsAdmin, self).save_model(request, obj, form, change)
