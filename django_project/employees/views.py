from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Employee, EmployeeImage


class EmployeeListViews(ListView):
    model = Employee
    template_name = "employees/employee_list.html"  # 'employees/list.html'
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        # Используем prefetch_related для оптимизации запросов
        return super().get_queryset().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущую страницу
        page = context['page_obj']

        # Для каждого сотрудника находим основное фото
        employees_data = []
        for employee in context['employees']:
            main_photo = employee.images.filter(is_main=True).first()
            employees_data.append({
                'emp': employee,  # объект сотрудника
                'main_photo': main_photo  # основное фото или None
            })

        context['employees_data'] = employees_data
        return context


class EmployeeDetailViews(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_details.html"
    context_object_name = "emp"

    @staticmethod
    def get_sorted_images(employee, sort_order):
        """Получение отсортированных изображений"""
        if sort_order == "desc":
            return employee.images.all().order_by("-order")
        return employee.images.all().order_by("order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emp = self.object
        main_photo = emp.images.filter(is_main=True).first()

        # Сортировка
        sort_order = self.request.GET.get("sort", "asc")
        images = self.get_sorted_images(emp, sort_order)

        context.update({
            'images': images,
            "current_sort": sort_order,
            'main_photo': main_photo,
        })

        return context

class EmployeeImageMixin:
    """Миксин для работы с изображениями сотрудника"""
    @staticmethod
    def get_employee(pk):
        """Получение сотрудника"""
        return get_object_or_404(Employee, pk=pk)

    @staticmethod
    def get_image(image_pk):
        """Получение изображения с проверкой принадлежности сотруднику"""
        return get_object_or_404(EmployeeImage, pk=image_pk)

    @staticmethod
    def set_main_photo(image, employee):
        """установка главного фото"""
        EmployeeImage.objects.filter(
            employee=employee,
            is_main=True
        ).update(is_main=False)
        image.is_main = True
        image.save()

    @staticmethod
    def create_employee_image(employee, image_file, order=None, make_main=False):
        """Создание нового изображения"""
        employee_image = EmployeeImage(
            employee=employee,
            image=image_file,
            order=order
        )

        if make_main:
            EmployeeImageMixin.set_main_photo(employee_image, employee)

        employee_image.save()
        return employee_image

"""==============================================================================="""

def add_employee_image(request, pk):
    """Добавляем фото"""
    if request.method == 'POST':
        employee = EmployeeImageMixin.get_employee(pk)
        image_file = request.FILES.get('image')
        order = request.POST.get('order')
        make_main = request.POST.get('is_main') == 'on'

        if image_file:
            EmployeeImageMixin.create_employee_image(
                employee, image_file, order, make_main
            )
            messages.success(request, 'Изображение успешно добавлено')
        else:
            messages.error(request, 'Выберите файл для загрузки')

    return redirect('employees:detail', pk=pk)

def set_main_photo(request, pk):
    """Установка главного фото"""
    if request.method == 'POST':
        image_pk = request.POST.get('image_pk')
        employee = EmployeeImageMixin.get_employee(pk)

        image = EmployeeImageMixin.get_image(image_pk)
        EmployeeImageMixin.set_main_photo(image, employee)
        messages.success(request, 'Главное фото обновлено')

    return redirect('employees:detail', pk=pk)

def delete_employee_image(request, pk):
    """Удаление фото"""
    if request.method == 'POST':
        image_pk = request.POST.get('image_pk')
        image = EmployeeImageMixin.get_image(image_pk)
        image.delete()
        messages.success(request, 'Изображение удалено')

    return redirect('employees:detail', pk=pk)
