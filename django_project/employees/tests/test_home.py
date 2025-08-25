from django.test import TestCase
from django.urls import reverse
# noinspection PyUnresolvedReferences
from employees.models import Employee, EmployeeSkill
# noinspection PyUnresolvedReferences
from workplaces.models import Workplace


class HomePageTests(TestCase):
    """Тесты для главной страницы"""

    def setUp(self):
        # Создаем тестовых сотрудников
        self.employee1 = Employee.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов',
            gender='M'
        )
        self.employee2 = Employee.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Петр',
            last_name='Петров',
            gender='M'
        )

        # Добавляем навыки
        EmployeeSkill.objects.create(
            employee=self.employee1,
            skill='backend',
            level=8
        )
        EmployeeSkill.objects.create(
            employee=self.employee2,
            skill='frontend',
            level=7
        )

    def test_home_page_status_code(self):
        """Тест доступности главной страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_context(self):
        """Тест контекста главной страницы"""
        response = self.client.get(reverse('home'))

        # Проверяем наличие ключевых данных в контексте
        self.assertIn('latest_employees', response.context)

        # Проверяем структуру данных сотрудников
        if response.context['latest_employees']:
            employee_data = response.context['latest_employees'][0]
            self.assertIn('employee', employee_data)
            self.assertIn('main_photo', employee_data)
            self.assertIn('experience_days', employee_data)

    def test_home_page_shows_latest_employees(self):
        """Тест отображения последних сотрудников"""
        response = self.client.get(reverse('home'))

        # Должны отображаться последние 4 сотрудника
        self.assertLessEqual(len(response.context['latest_employees']), 4)