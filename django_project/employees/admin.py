from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# noinspection PyUnresolvedReferences
from import_export import resources
# noinspection PyUnresolvedReferences
from import_export.admin import ImportExportModelAdmin

from .models import Employee, EmployeeImage, EmployeeSkill


class EmployeesResource(resources.ModelResource):
    class Meta:
        model = Employee


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 0


class EmployeeImageInline(admin.TabularInline):  # или admin.StackedInline
    model = EmployeeImage
    extra = 0  # Количество пустых форм для добавления
    fields = ["image", "order", "created_at"]
    readonly_fields = ["created_at"]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Скрываем поле order при добавлении - он заполнится автоматически
        formset.form.base_fields["order"].widget.attrs["style"] = "display: none"
        formset.form.base_fields["order"].label = ""
        return formset


@admin.register(Employee)
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = EmployeesResource
    # filter_horizontal = ('groups', 'user_permissions')
    list_display = (
        "username",
        "email",
        "last_name",
        "first_name",
        "middle_name",
        "gender",
        "show_skills",
        "is_staff",
        #'cover',
    )
    list_display_links = ("username", "email")  # Кликабельные объекты
    list_editable = ("last_name", "first_name", "middle_name")
    search_fields = (
        "username__iexact",  # Точный поиск (но нечувствительный к регистру)
        "email__icontains",  # Частичный поиск (чувствительный к регистру)
        "last_name__iexact",  # Точный поиск (но нечувствительный к регистру)
        "first_name__iexact",  # Точный поиск (но нечувствительный к регистру)
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
    inlines = [EmployeeSkillInline, EmployeeImageInline]

    def show_skills(self, obj):
        skills = obj.skills.all()
        return (
            ", ".join([f"{es.get_skill_display()} ({es.level})" for es in skills])
            if skills
            else "Нет навыков"
        )

    show_skills.short_description = "Навыки"

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        skill_map = {
            "бэкенд": "backend",
            "фронтенд": "frontend",
            "тестирование": "testing",
            "Управление проектами": "management",
            "Дизайн": "design",
            "devops": "DevOps",
        }
        lower_search = search_term.lower().strip()
        if lower_search in skill_map:
            queryset |= self.model.objects.filter(skills__skill=skill_map[lower_search])

        return queryset, use_distinct


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = (
        "employee_info",
        "skill",
        "level",
    )
    list_filter = ("skill",)
    search_fields = (
        "employee__username",
        "skill",
    )

    def employee_info(self, obj):
        return f"{obj.employee.last_name} {obj.employee.first_name} ({obj.employee.username})"

    employee_info.short_description = "Сотрудник"


# admin.site.register(Employee, EmployeeAdmin)
