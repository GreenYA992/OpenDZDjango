# noinspection PyUnresolvedReferences
from rest_framework import viewsets, filters, status, permissions
# noinspection PyUnresolvedReferences
from rest_framework.decorators import action
# noinspection PyUnresolvedReferences
from rest_framework.response import Response
# noinspection PyUnresolvedReferences
from rest_framework.permissions import IsAuthenticated, AllowAny
# noinspection PyUnresolvedReferences
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import datetime

from .models import Employee, EmployeeSkill
from workplaces.models import Workplace
from .serializers import EmployeeSerializer
from workplaces.serializers import WorkplaceSerializer
# noinspection PyUnresolvedReferences
from .permissions import IsViewer, IsAdmin


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().prefetch_related('skills', 'images')
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['gender', 'skills__skill']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering_fields = ['date_joined', 'last_name', 'first_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по стажу
        min_experience = self.request.query_params.get('min_experience')
        max_experience = self.request.query_params.get('max_experience')

        if min_experience or max_experience:
            today = now().date()
            queryset = queryset.filter(is_active=True)

            if min_experience:
                min_date = today - datetime.timedelta(days=int(min_experience))
                queryset = queryset.filter(date_joined__date__lte=min_date)

            if max_experience:
                max_date = today - datetime.timedelta(days=int(max_experience))
                queryset = queryset.filter(date_joined__date__gte=max_date)

        # Фильтрация по навыкам
        skills = self.request.query_params.get('skills')
        if skills:
            skill_list = skills.split(',')
            queryset = queryset.filter(skills__skill__in=skill_list).distinct()

        return queryset

    @action(detail=False, methods=['get'])
    def filters(self, request):
        """Доступные фильтры"""
        return Response({
            'genders': dict(Employee.GENDER_CHOICES),
            'skills': dict(EmployeeSkill.SKILL_CHOICES),
        })


class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]  # Все аутентифицированные
        elif self.action in ['update', 'partial_update']:  # Перемещение сотрудников
            permission_classes = [IsViewer]  # Только смотритель и админ
        else:
            permission_classes = [IsAdmin]  # Только админ
        return [permission() for permission in permission_classes]