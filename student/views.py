from . import models
from django.views.generic import (ListView, CreateView)


class StudentListView(ListView):
    context_object_name = 'students'
    model = models.Student


class StudentCreateView(CreateView):
    fields = '__all__'
    template_name = 'student/student_form.html'
    model = models.Student
