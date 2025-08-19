from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Employee(AbstractUser):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]
    email = models.EmailField(unique=True, verbose_name="Email", blank=False,)
    username = models.CharField(max_length=150, unique=True, verbose_name="Логин",)
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover = models.ImageField(upload_to='covers/', blank=True)

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
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        #app_label = 'auth'

    def save(self, *args, **kwargs):
        # Приводим email к нижнему регистру перед сохранением
        # noinspection PyUnresolvedReferences
        self.email = self.email.lower() if self.email else self.email
        super().save(*args, **kwargs)

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
