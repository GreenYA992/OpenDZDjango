from django.db import models
from employees.models import Employee


class Workplace(models.Model):
    desk_number = models.CharField(max_length=10, unique=True, verbose_name="Номер стола")
    employee = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workplace',  # Добавляем related_name
        verbose_name="Сотрудник",
    )
    additional_info = models.TextField(blank=True, verbose_name="Дополнительная информация")

    class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

    def __str__(self):
        return f"Рабочее место #{self.desk_number}"
