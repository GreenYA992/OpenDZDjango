from django.http import HttpResponse
from django.shortcuts import render

from .models import Employee

from django.views.generic import DetailView, ListView


def index(request):
    template_name = None # 'employees/index.html'
    context = {
        'employees': Employee.objects.all()
    }
    return render(request, template_name, context)

def detail(request, pk):
    template_name = None # 'employees/detail.html'
    context = {
        'employees': Employee.objects.get(pk=pk)
    }
    return render(request, template_name, context)


class EmployeeListViews(ListView):
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees'

class EmployeeDetailViews(DetailView):
    model = Employee
    template_name = 'employees/details.html'
    context_object_name = 'emp'
