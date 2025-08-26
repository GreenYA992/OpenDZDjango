from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from employees.models import Employee
from workplaces.models import Workplace


class Command(BaseCommand):
    help = 'Create default user groups'

    def handle(self, *args, **options):
        # Группа Посетителей
        visitor_group, created = Group.objects.get_or_create(name='Посетитель')

        # Группа Смотрителей
        viewer_group, created = Group.objects.get_or_create(name='Смотритель')
        # Добавить права на изменение рабочих мест
        content_type = ContentType.objects.get_for_model(Workplace)
        change_permission = Permission.objects.get(
            content_type=content_type,
            codename='change_workplace'
        )
        viewer_group.permissions.add(change_permission)

        # Группа Администраторов
        admin_group, created = Group.objects.get_or_create(name='Администратор')
        # Все права на сотрудников и рабочие места
        employee_content_type = ContentType.objects.get_for_model(Employee)
        workplace_content_type = ContentType.objects.get_for_model(Workplace)

        for perm in Permission.objects.filter(
                content_type__in=[employee_content_type, workplace_content_type]
        ):
            admin_group.permissions.add(perm)

        self.stdout.write('Группы пользователей созданы!')