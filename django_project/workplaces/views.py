from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Workplace

class WorkplaceListViews(ListView):
    model = Workplace
    template_name = "workplaces/booking.html"
    context_object_name = "workplaces"


