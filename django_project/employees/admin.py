from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Skill, EmployeeSkill

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(Employee)
class CustomUserAdmin(UserAdmin):
    # Переносим сотрудников в раздел "Пользователи и группы"
    # app_label = "auth"

    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'gender', 'show_skills')
    list_editable = ('last_name', 'first_name', 'middle_name')
    """"""
    # Дополнительная информация, если выбрать сотрудника
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('middle_name', 'gender', 'description')}),
    )
    # Навыки, если выбрать сотрудника
    inlines = [EmployeeSkillInline]


    def show_skills(self, obj):
        return ", ".join([f"{es.skill.name} ({es.level})" for es in obj.skills.all()])
    show_skills.short_description = "Навыки"

admin.site.register(Skill)
admin.site.register(EmployeeSkill)
