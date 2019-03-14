from . import models
from django.shortcuts import reverse
from .forms import CourseForm, Subject_Form
from django.views.generic import CreateView


class CourseCreateView(CreateView):
    form_class = CourseForm
    template_name = 'course/course_form.html'
    model = models.Course

    def get_success_url(self):
        return reverse('home')


class SubjectCreateView(CreateView):
    form_class = Subject_Form
    template_name = 'subject/subject_form.html'
    model = models.Subject

    def get_success_url(self):
        return reverse('home')
