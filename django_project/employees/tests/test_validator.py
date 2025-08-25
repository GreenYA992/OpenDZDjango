from django.test import TestCase
from django.core.exceptions import ValidationError
# noinspection PyUnresolvedReferences
from employees.models import Employee, EmployeeSkill
# noinspection PyUnresolvedReferences
from workplaces.models import Workplace


class WorkplaceValidatorTests(TestCase):
    """Тесты валидатора рабочих мест"""

    def setUp(self):
        # Создаем разработчика
        self.developer = Employee.objects.create_user(
            username='developer',
            email='dev@example.com',
            password='testpass123',
            first_name='Разработчик',
            last_name='Тестовый',
            gender='M'
        )
        EmployeeSkill.objects.create(
            employee=self.developer,
            skill='backend',
            level=9
        )

        # Создаем тестировщика
        self.tester = Employee.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='testpass123',
            first_name='Тестировщик',
            last_name='Тестовый',
            gender='F'
        )
        EmployeeSkill.objects.create(
            employee=self.tester,
            skill='testing',
            level=8
        )

        # Создаем другого разработчика
        self.another_developer = Employee.objects.create_user(
            username='dev2',
            email='dev2@example.com',
            password='testpass123',
            first_name='Другой',
            last_name='Разработчик',
            gender='M'
        )
        EmployeeSkill.objects.create(
            employee=self.another_developer,
            skill='frontend',
            level=7
        )

        # Создаем менеджера (не разработчик и не тестировщик)
        self.manager = Employee.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='testpass123',
            first_name='Менеджер',
            last_name='Тестовый',
            gender='F'
        )
        EmployeeSkill.objects.create(
            employee=self.manager,
            skill='management',
            level=10
        )

    def test_developer_and_tester_cannot_be_neighbors(self):
        """Тест, что разработчик и тестировщик не могут быть на соседних столах"""
        # Создаем рабочие места
        desk1 = Workplace.objects.create(desk_number='1')
        desk2 = Workplace.objects.create(desk_number='2')

        # Размещаем разработчика на первом столе
        desk1.employee = self.developer
        desk1.save()

        # Пытаемся разместить тестировщика на соседнем столе - должна быть ошибка
        desk2.employee = self.tester
        with self.assertRaises(ValidationError) as context:
            desk2.full_clean()

        self.assertIn('Нельзя размещать разработчиков и тестировщиков на соседних столах', str(context.exception))

    def test_tester_and_developer_cannot_be_neighbors(self):
        """Тест, что тестировщик и разработчик не могут быть на соседних столах (обратный случай)"""
        desk1 = Workplace.objects.create(desk_number='1')
        desk2 = Workplace.objects.create(desk_number='2')

        # Размещаем тестировщика на первом столе
        desk1.employee = self.tester
        desk1.save()

        # Пытаемся разместить разработчика на соседнем столе - должна быть ошибка
        desk2.employee = self.developer
        with self.assertRaises(ValidationError) as context:
            desk2.full_clean()

        self.assertIn('Нельзя размещать разработчиков и тестировщиков на соседних столах', str(context.exception))

    def test_developers_can_be_neighbors(self):
        """Тест, что два разработчика могут быть на соседних столах"""
        desk1 = Workplace.objects.create(desk_number='1')
        desk2 = Workplace.objects.create(desk_number='2')

        # Размещаем первого разработчика
        desk1.employee = self.developer
        desk1.save()

        # Размещаем второго разработчика - не должно быть ошибки
        desk2.employee = self.another_developer
        try:
            desk2.full_clean()
            desk2.save()
        except ValidationError:
            self.fail("Два разработчика должны могут быть на соседних столах")

    def test_testers_can_be_neighbors(self):
        """Тест, что два тестировщика могут быть на соседних столах"""
        # Создаем второго тестировщика
        another_tester = Employee.objects.create_user(
            username='tester2',
            email='tester2@example.com',
            password='testpass123',
            first_name='Другой',
            last_name='Тестировщик',
            gender='M'
        )
        EmployeeSkill.objects.create(
            employee=another_tester,
            skill='testing',
            level=7
        )

        desk1 = Workplace.objects.create(desk_number='1')
        desk2 = Workplace.objects.create(desk_number='2')

        # Размещаем первого тестировщика
        desk1.employee = self.tester
        desk1.save()

        # Размещаем второго тестировщика - не должно быть ошибки
        desk2.employee = another_tester
        try:
            desk2.full_clean()
            desk2.save()
        except ValidationError:
            self.fail("Два тестировщика должны могут быть на соседних столах")

    def test_non_conflicting_roles_can_be_neighbors(self):
        """Тест, что неконфликтующие роли могут быть на соседних столах"""
        desk1 = Workplace.objects.create(desk_number='1')
        desk2 = Workplace.objects.create(desk_number='2')

        # Размещаем разработчика
        desk1.employee = self.developer
        desk1.save()

        # Размещаем менеджера - не должно быть ошибки
        desk2.employee = self.manager
        try:
            desk2.full_clean()
            desk2.save()
        except ValidationError:
            self.fail("Разработчик и менеджер должны могут быть на соседних столах")

    def test_employee_cannot_have_multiple_workplaces(self):
        """Тест, что сотрудник не может занимать несколько рабочих мест"""
        desk1 = Workplace.objects.create(desk_number='1')
        desk2 = Workplace.objects.create(desk_number='2')

        # Размещаем сотрудника на первом столе
        desk1.employee = self.developer
        desk1.save()

        # Пытаемся разместить того же сотрудника на втором столе - должна быть ошибка
        desk2.employee = self.developer
        with self.assertRaises(ValidationError) as context:
            desk2.full_clean()

        self.assertIn('уже забронировал рабочее место', str(context.exception))