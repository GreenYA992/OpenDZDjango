from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Skill, EmployeeSkill

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(Employee)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'gender')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('middle_name', 'gender', 'description')}),
    )
    inlines = [EmployeeSkillInline]

admin.site.register(Skill)
admin.site.register(EmployeeSkill)
