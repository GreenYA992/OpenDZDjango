# noinspection PyUnresolvedReferences
from rest_framework import serializers
from .models import Employee, EmployeeSkill, EmployeeImage
from django.contrib.auth.hashers import make_password


class EmployeeSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'level']


class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ['image', 'order', 'is_main', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(many=True, read_only=True)
    images = EmployeeImageSerializer(many=True, read_only=True)
    experience_full = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'middle_name', 'gender', 'description', 'skills', 'images',
            'experience_full', 'date_joined', 'is_staff'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)