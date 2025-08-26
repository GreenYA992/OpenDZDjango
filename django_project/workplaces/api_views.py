# noinspection PyUnresolvedReferences
from rest_framework import viewsets, permissions, status
# noinspection PyUnresolvedReferences
from rest_framework.decorators import action
# noinspection PyUnresolvedReferences
from rest_framework.response import Response
from .models import Workplace
from .serializers import WorkplaceSerializer, WorkplaceAssignSerializer
# noinspection PyUnresolvedReferences
from employees.permissions import IsViewer, IsAdmin


class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.all().select_related('employee')
    serializer_class = WorkplaceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Просмотр - все аутентифицированные
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'assign_employee']:
            # Изменение - смотритель и админ
            permission_classes = [IsViewer]
        else:
            # Создание, удаление - только админ
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['assign_employee']:
            return WorkplaceAssignSerializer
        return WorkplaceSerializer

    @action(detail=True, methods=['patch'])
    def assign_employee(self, request, pk=None):
        """Специальное действие для назначения сотрудника на рабочее место"""
        workplace = self.get_object()
        serializer = self.get_serializer(workplace, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        """Освободить рабочее место"""
        workplace = self.get_object()
        workplace.employee = None
        workplace.save()

        serializer = self.get_serializer(workplace)
        return Response(serializer.data)