from django.contrib import admin
from webapp.models import List, Status, Type
# Register your models here.


class ListAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'updated_at']
    list_filter = ['status', 'tip']
    search_fields = ['summary']
    fields = ['id', 'summary', 'description', 'status', 'tip', 'updated_at']
    readonly_fields = ['updated_at', 'id']


admin.site.register(List, ListAdmin)
admin.site.register(Status)
admin.site.register(Type)
