from django.contrib import admin
from .models import Branches
from .models import Notice
from .models import NoticiesDocs

@admin.register(Branches)
class BranchesAdmin(admin.ModelAdmin):
    list_display = ('title', 'license_num', 'address', 'phone')
    list_display_links = ('title',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published', 'creator', 'get_filials_str',)
    list_display_links = ('title',)
    search_fields = ('title', 'content',)
    readonly_fields = ('creator',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.set_creator(obj.user)
        super(NoticeAdmin, self).save_model(request, obj, form, change)

@admin.register(NoticiesDocs)
class NoticiesDocsAdmin(admin.ModelAdmin):
    list_display = ('notice', 'first_name', 'document', 'published', 'creator', )
    readonly_fields = ('published', 'creator',)
    list_display_links = ('first_name',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.set_creator(obj.user)
        obj.first_name = obj.document.name
        super(NoticiesDocsAdmin, self).save_model(request, obj, form, change)
