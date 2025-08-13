from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Skill(models.Model):
    name = models.CharField(
        max_length=100,
        #verbose_name="Навык",
        choices=[
            ('frontend', 'Фронтенд'),
            ('backend', 'Бэкенд'),
            ('testing', 'Тестирование'),
            ('management', 'Управление проектами'),
            ('design', 'Дизайн'),
            ('devops', 'DevOps'),
            ],
        unique=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    #last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    #first_name = models.CharField(max_length=100, blank=True, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='skills',  # Важно: используем related_name
        verbose_name="Сотрудник"
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name="Навык"
    )
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень навыка"
    )

    class Meta:
        unique_together = ('employee', 'skill')  # Один навык на сотрудника
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"

    def __str__(self):
        return f"{self.employee} - {self.skill} (уровень {self.level})"
