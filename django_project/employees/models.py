from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta


class Employee(AbstractUser):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        blank=False,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
    )
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    description = models.TextField(blank=True, verbose_name="Описание")

    """
    groups = models.ManyToManyField(
        Group,
        verbose_name="Группы",
        blank=True,
        related_name="employee_groups",  # чтобы избежать конфликтов
        related_query_name="employees",
    )
    """

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        # app_label = 'auth'

    def save(self, *args, **kwargs):
        # Приводим email к нижнему регистру перед сохранением
        # noinspection PyUnresolvedReferences
        self.email = self.email.lower() if self.email else self.email
        super().save(*args, **kwargs)

    @property
    def experience_full(self):
        """Полный стаж в годах, месяцах и днях от даты регистрации"""
        delta = relativedelta(now().date(), self.date_joined.date())
        if self.is_active:
            return f"{delta.years} лет {delta.months} месяцев {delta.days} дней"
        return "уволен"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class EmployeeSkill(models.Model):
    SKILL_CHOICES = [
        ("frontend", "Фронтенд"),
        ("backend", "Бэкенд"),
        ("testing", "Тестирование"),
        ("management", "Управление проектами"),
        ("design", "Дизайн"),
        ("devops", "DevOps"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name="Сотрудник",
    )
    skill = models.CharField(
        max_length=100, choices=SKILL_CHOICES, verbose_name="Навык"
    )
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень навыка",
    )

    class Meta:
        unique_together = ("employee", "skill")
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return f"{self.employee} - {self.get_skill_display()} (уровень {self.level})"


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Сотрудник",
    )

    image = models.ImageField(
        upload_to="covers/", blank=True, verbose_name="Изображение"
    )

    order = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Порядковый номер",
        help_text="Чем меньше число, тем выше в галерее",
    )

    is_main = models.BooleanField(
        default=False,
        verbose_name="Главное фото",
        help_text="Использовать как главное фото сотрудника сотрудника"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.order is None:  # Если order не указан
            # Находим максимальный order для этого сотрудника
            max_order = (
                EmployeeImage.objects.filter(employee=self.employee).aggregate(
                    models.Max("order")
                )["order__max"]
                or 0
            )
            self.order = max_order + 1
        super().save(*args, **kwargs)

        # Если это фото становится главным, снимаем флаг с других фото
        if self.is_main:
            EmployeeImage.objects.filter(
                employee=self.employee,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("employee", "order")
        ordering = ("order", "created_at")
        verbose_name = "файл сотрудника"
        verbose_name_plural = "файлы сотрудников"

    def __str__(self):
        status = " (Главное)" if self.is_main else ""
        return f"Изображение {self.order} для {self.employee}{status}"
