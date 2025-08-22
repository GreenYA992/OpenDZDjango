from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .models import Workplace
from employees.models import Employee

class WorkplaceListViews(ListView):
    model = Workplace
    template_name = "workplaces/booking.html"
    context_object_name = "workplaces"








    def get_queryset(self):
        return Workplace.objects.select_related('employee').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_employees'] = Employee.objects.filter(
            workplace__isnull=True
        ).prefetch_related('skills')
        return context


class WorkplaceBookView(LoginRequiredMixin, UpdateView):
    model = Workplace
    fields = []  # Не нужны поля, так как мы только назначаем сотрудника
    template_name = 'workplaces/workplace_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_employees'] = Employee.objects.filter(
            workplace__isnull=True
        ).prefetch_related('skills')
        return context

    def form_valid(self, form):
        employee_id = self.request.POST.get('employee_id')

        if not employee_id:
            form.add_error(None, 'Не выбран сотрудник')
            return self.form_invalid(form)

        try:
            employee = Employee.objects.get(pk=employee_id)
            self.object.employee = employee

            try:
                # Вызовет валидацию, включая проверку соседних столов
                self.object.full_clean()
                self.object.save()

                messages.success(
                    self.request,
                    f'Рабочее место #{self.object.desk_number} '
                    f'успешно забронировано для {employee}'
                )
                return redirect('workplaces:workplace-list')

            except ValidationError as e:
                form.add_error(None, e.message)
                return self.form_invalid(form)

        except Employee.DoesNotExist:
            form.add_error(None, 'Сотрудник не найден')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при бронировании рабочего места: ' +
            ', '.join([str(error) for error in form.non_field_errors()])
        )
        return super().form_invalid(form)


class WorkplaceReleaseView(LoginRequiredMixin, UpdateView):
    model = Workplace
    fields = []  # Не нужны поля
    template_name = 'workplaces/workplace_release.html'

    def form_valid(self, form):
        workplace = self.object
        employee_name = str(workplace.employee) if workplace.employee else "Неизвестный"

        workplace.employee = None
        workplace.save()

        messages.success(
            self.request,
            f'Рабочее место #{workplace.desk_number} освобождено от {employee_name}'
        )
        return redirect('workplaces:workplace-list')


class WorkplaceCreateView(LoginRequiredMixin, CreateView):
    model = Workplace
    fields = ['desk_number', 'additional_info']
    template_name = 'workplaces/workplace_form.html'
    success_url = reverse_lazy('workplaces:workplace-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Рабочее место #{form.instance.desk_number} успешно создано'
        )
        return super().form_valid(form)


class WorkplaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Workplace
    template_name = 'workplaces/workplace_confirm_delete.html'
    success_url = reverse_lazy('workplaces:workplace-list')

    def delete(self, request, *args, **kwargs):
        workplace = self.get_object()
        messages.success(
            request,
            f'Рабочее место #{workplace.desk_number} удалено'
        )
        return super().delete(request, *args, **kwargs)


def workplace_detail(request, pk):
    workplace = get_object_or_404(Workplace.objects.select_related('employee'), pk=pk)

    # Получаем информацию о соседних столах
    neighbor_desks = workplace.get_neighbor_tables()
    neighbors = Workplace.objects.filter(
        desk_number__in=neighbor_desks
    ).select_related('employee')

    context = {
        'workplace': workplace,
        'neighbors': neighbors,
    }

    return render(request, 'workplaces/workplace_detail.html', context)


