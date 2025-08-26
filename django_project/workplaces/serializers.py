# noinspection PyUnresolvedReferences
from rest_framework import serializers
from .models import Workplace
# noinspection PyUnresolvedReferences
from employees.serializers import EmployeeSerializer  # для связанных данных


class WorkplaceSerializer(serializers.ModelSerializer):
    # Добавляем подробную информацию о сотруднике
    employee_info = serializers.SerializerMethodField()

    class Meta:
        model = Workplace
        fields = [
            'id',
            'desk_number',
            'employee',
            'employee_info',
            'additional_info'
        ]
        read_only_fields = ['employee_info']

    def get_employee_info(self, obj):
        if obj.employee:
            return {
                'id': obj.employee.id,
                'username': obj.employee.username,
                'full_name': f"{obj.employee.last_name} {obj.employee.first_name}",
                'skills': obj.employee.get_skills_display(),
            }
        return None


class WorkplaceAssignSerializer(serializers.ModelSerializer):
    """Сериализатор для назначения сотрудника на рабочее место"""

    class Meta:
        model = Workplace
        fields = ['employee']