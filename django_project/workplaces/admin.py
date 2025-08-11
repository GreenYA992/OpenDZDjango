from django.contrib import admin
from .models import Workplace

@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('desk_number', 'employee', 'additional_info')
    list_filter = ('desk_number',)
    search_fields = ('desk_number', 'employee__last_name')
