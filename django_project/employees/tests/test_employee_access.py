from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# noinspection PyUnresolvedReferences
from employees.models import Employee, EmployeeSkill

User = get_user_model()


class EmployeeAccessTests(TestCase):
    """Тесты прав доступа к страницам сотрудников"""

    def setUp(self):
        # Создаем обычного пользователя
        self.user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123',
            first_name='Обычный',
            last_name='Пользователь',
            gender='M'
        )

        # Создаем другого сотрудника для тестирования доступа
        self.other_employee = User.objects.create_user(
            username='otheremployee',
            email='other@example.com',
            password='testpass123',
            first_name='Другой',
            last_name='Сотрудник',
            gender='F'
        )

    def test_employee_detail_access_authenticated(self):
        """Тест доступа к детальной странице для аутентифицированных пользователей"""
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(
            reverse('employees:detail', kwargs={'pk': self.other_employee.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_employee_detail_access_unauthenticated(self):
        """Тест редиректа для неаутентифицированных пользователей"""
        response = self.client.get(
            reverse('employees:detail', kwargs={'pk': self.other_employee.pk})
        )
        # Должен быть редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_employee_detail_template_authenticated(self):
        """Тест шаблона для аутентифицированных пользователей"""
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(
            reverse('employees:detail', kwargs={'pk': self.other_employee.pk})
        )
        self.assertTemplateUsed(response, 'employees/employee_details.html')

    def test_employee_detail_context_authenticated(self):
        """Тест контекста детальной страницы"""
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(
            reverse('employees:detail', kwargs={'pk': self.other_employee.pk})
        )

        # Проверяем ключевые данные в контексте
        self.assertIn('emp', response.context)
        self.assertIn('images', response.context)
        self.assertIn('current_sort', response.context)
        self.assertIn('main_photo', response.context)

        # Проверяем, что отображается правильный сотрудник
        self.assertEqual(response.context['emp'], self.other_employee)

    def test_employee_actions_require_authentication(self):
        """Тест, что действия с изображениями требуют аутентификации"""
        urls_to_test = [
            reverse('employees:add_image', kwargs={'pk': self.other_employee.pk}),
            reverse('employees:set_main_photo', kwargs={'pk': self.other_employee.pk}),
            reverse('employees:delete_image', kwargs={'pk': self.other_employee.pk}),
        ]

        for url in urls_to_test:
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)