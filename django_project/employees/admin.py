from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# noinspection PyUnresolvedReferences
from .models import Employee, EmployeeSkill


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(Employee)
class CustomUserAdmin(UserAdmin):
#class EmployeeAdmin(UserAdmin):
    #filter_horizontal = ('groups', 'user_permissions')
    list_display = (
        "username",
        "email",
        "last_name",
        "first_name",
        "middle_name",
        "gender",
        "show_skills",
        'is_staff',
    )
    list_display_links = ('username', 'email') # Кликабельные объекты
    list_editable = ("last_name", "first_name", "middle_name")
    search_fields = (
        "username__iexact", # Точный поиск (но нечувствительный к регистру)
        "email__icontains", # Частичный поиск (чувствительный к регистру)
        "last_name__iexact", # Точный поиск (но нечувствительный к регистру)
        "first_name__iexact", # Точный поиск (но нечувствительный к регистру)
        "skills__skill__iexact",  # Точный поиск (но нечувствительный к регистру)

    )

    list_filter = ["skills__skill", "gender", "is_active"]
    # Поля в форме создания/редактирования
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {"fields": ("email", "first_name", "last_name", "middle_name", "gender")},
        ),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    # Поля при создании пользователя (админка)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    # Навыки, если выбрать сотрудника
    inlines = [EmployeeSkillInline]

    def show_skills(self, obj):
        skills = obj.skills.all()
        return (
            ", ".join([f"{es.get_skill_display()} ({es.level})" for es in skills])
            if skills
            else "Нет навыков"
        )

    show_skills.short_description = "Навыки"

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        skill_map = {
            'бэкенд': 'backend',
            'фронтенд': 'frontend',
            'тестирование': 'testing',
            'Управление проектами' : 'management',
            'Дизайн' : 'design',
            'devops' : 'DevOps',
        }
        lower_search = search_term.lower().strip()
        if lower_search in skill_map:
            queryset |= self.model.objects.filter(skills__skill=skill_map[lower_search])

        return queryset, use_distinct


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ('employee_info',
                    'skill',
                    'level',)
    list_filter = ('skill',)
    search_fields = ('employee__username', 'skill',)

    def employee_info(self, obj):
        return f"{obj.employee.last_name} {obj.employee.first_name} ({obj.employee.username})"

    employee_info.short_description = "Сотрудник"

#admin.site.register(Employee, EmployeeAdmin)
