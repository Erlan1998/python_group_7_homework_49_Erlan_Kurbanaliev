from django.contrib import admin
from webapp.models import List, Status, Type, Porjects
# Register your models here.


class ListAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'updated_at', 'project']
    list_filter = ['status', 'tip']
    search_fields = ['summary']
    fields = ['id', 'summary', 'description', 'status', 'tip', 'updated_at', 'project']
    readonly_fields = ['updated_at', 'id']


admin.site.register(List, ListAdmin)
admin.site.register(Porjects)
admin.site.register(Status)
admin.site.register(Type)
