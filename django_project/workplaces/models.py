from django.db import models
# noinspection PyUnresolvedReferences
from employees.models import Employee
from django.core.exceptions import ValidationError


class Workplace(models.Model):
    desk_number = models.CharField(
        max_length=10, unique=True, verbose_name="Номер стола"
    )
    employee = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workplace",  # Добавляем related_name
        verbose_name="Сотрудник",
    )
    additional_info = models.TextField(
        blank=True, verbose_name="Дополнительная информация"
    )

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"

    def __str__(self):
        return f"Рабочее место #{self.desk_number}"










    def clean(self):
        """Валидация при сохранении"""
        super().clean()

        if self.employee:
            # Проверяем, что сотрудник не забронировал уже другое место
            existing_workplace = Workplace.objects.filter(
                employee=self.employee
            ).exclude(pk=self.pk).first()

            if existing_workplace:
                raise ValidationError(
                    f"Сотрудник {self.employee} уже забронировал рабочее место #{existing_workplace.desk_number}"
                )

            # Проверяем соседние столы на конфликт разработчиков и тестировщиков
            self._validate_neighbor_tables()

    def _validate_neighbor_tables(self):
        """Проверка соседних столов на конфликт разработчиков и тестировщиков"""
        current_desk_num = int(self.desk_number) if self.desk_number.isdigit() else 0

        # Получаем номера соседних столов
        neighbor_desks = [
            str(current_desk_num - 1),
            str(current_desk_num + 1)
        ]

        # Находим соседние рабочие места
        neighbor_workplaces = Workplace.objects.filter(
            desk_number__in=neighbor_desks
        ).exclude(employee__isnull=True).exclude(pk=self.pk)

        current_employee_skills = set(
            self.employee.skills.all().values_list('skill', flat=True)
        )

        for neighbor in neighbor_workplaces:
            neighbor_skills = set(
                neighbor.employee.skills.all().values_list('skill', flat=True)
            )

            # Проверяем конфликт: разработчик и тестировщик на соседних столах
            has_developer = any(skill in ['frontend', 'backend'] for skill in current_employee_skills)
            has_tester = 'testing' in current_employee_skills

            neighbor_has_developer = any(skill in ['frontend', 'backend'] for skill in neighbor_skills)
            neighbor_has_tester = 'testing' in neighbor_skills

            # Конфликт: разработчик рядом с тестировщиком
            if (has_developer and neighbor_has_tester) or (has_tester and neighbor_has_developer):
                raise ValidationError(
                    f"Нельзя размещать разработчиков и тестировщиков на соседних столах! "
                    f"Стол #{neighbor.desk_number} занят {neighbor.employee} "
                    f"({neighbor.employee.get_skills_display()})"
                )

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова полной валидации"""
        self.full_clean()  # Вызывает clean() и все валидаторы
        super().save(*args, **kwargs)

    def get_neighbor_tables(self):
        """Получить соседние столы"""
        try:
            current_desk_num = int(self.desk_number)
            return [
                str(current_desk_num - 1),
                str(current_desk_num + 1)
            ]
        except ValueError:
            return []


