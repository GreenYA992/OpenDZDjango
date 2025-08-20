from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Employee


class EmployeeListViews(ListView):
    model = Employee
    template_name = "employees/employee_list.html"  # 'employees/list.html'
    context_object_name = "employees"


class EmployeeDetailViews(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_details.html"  # 'employees/details.html'
    context_object_name = "emp"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emp = self.object
        main_photo = emp.images.filter(is_main=True).first()

        # Получаем параметр сортировки
        sort_order = self.request.GET.get("sort", "asc")

        # Сортируем изображения
        if sort_order == "desc":
            images = emp.images.all().order_by("-order")
        else:
            images = emp.images.all().order_by("order")

        context = {
            'emp': emp,
            'images': images,
            "current_sort": sort_order,
            'main_photo': main_photo,
        }
        #context["images"] = images
        #context["current_sort"] = sort_order
        return context
