from django.test import TestCase
from django.urls import reverse
# noinspection PyUnresolvedReferences
from employees.models import Employee, EmployeeSkill


class EmployeeListViewTests(TestCase):
    """Тесты для списка сотрудников"""

    def setUp(self):
        # Создаем нескольких сотрудников
        for i in range(15):
            employee = Employee.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass123',
                first_name=f'Имя{i}',
                last_name=f'Фамилия{i}',
                gender='M' if i % 2 == 0 else 'F'
            )
            # Добавляем навыки
            skill = 'backend' if i % 3 == 0 else 'frontend' if i % 3 == 1 else 'testing'
            EmployeeSkill.objects.create(
                employee=employee,
                skill=skill,
                level=i % 10 + 1
            )

    def test_employee_list_status_code(self):
        """Тест доступности списка сотрудников"""
        response = self.client.get(reverse('employees:list'))
        self.assertEqual(response.status_code, 200)

    def test_employee_list_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('employees:list'))
        self.assertTemplateUsed(response, 'employees/employee_list.html')

    def test_employee_list_context(self):
        """Тест контекста списка сотрудников"""
        response = self.client.get(reverse('employees:list'))

        # Проверяем наличие ключевых данных в контексте
        self.assertIn('employees_data', response.context)
        self.assertIn('total_count', response.context)
        self.assertIn('current_page_count', response.context)
        self.assertIn('page_obj', response.context)

        # Проверяем корректность данных
        self.assertEqual(response.context['total_count'], 15)
        self.assertEqual(response.context['current_page_count'], 10)  # paginate_by = 10

    def test_employee_list_pagination(self):
        """Тест пагинации списка сотрудников"""
        response = self.client.get(reverse('employees:list'))
        self.assertTrue(response.context['is_paginated'])

        # Проверяем вторую страницу
        response_page2 = self.client.get(reverse('employees:list') + '?page=2')
        self.assertEqual(response_page2.context['page_obj'].number, 2)
        self.assertEqual(response_page2.context['current_page_count'], 5)

    def test_employee_list_contains_employees(self):
        """Тест отображения сотрудников в списке"""
        response = self.client.get(reverse('employees:list'))

        # Проверяем, что сотрудники отображаются
        self.assertTrue(len(response.context['employees_data']) > 0)

        # Проверяем структуру данных каждого сотрудника
        for employee_data in response.context['employees_data']:
            self.assertIn('emp', employee_data)
            self.assertIn('main_photo', employee_data)
            self.assertIsInstance(employee_data['emp'], Employee)