from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Employee

from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class EmployeeListViews(ListView):
    model = Employee
    template_name = 'employees/employee_list.html' # 'employees/list.html'
    context_object_name = 'employees'

class EmployeeDetailViews(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_details.html' # 'employees/details.html'
    context_object_name = 'emp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.object

        # Получаем параметр сортировки
        sort_order = self.request.GET.get('sort', 'asc')

        # Сортируем изображения
        if sort_order == 'desc':
            images = employee.images.all().order_by('-order')
        else:
            images = employee.images.all().order_by('order')

        context['images'] = images
        context['current_sort'] = sort_order
        return context
