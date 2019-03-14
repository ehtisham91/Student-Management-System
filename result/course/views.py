from . import models
from django.shortcuts import reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.core.urlresolvers import reverse_lazy
# from django.views.generic import (View,ListView,
#                                 DetailView,TemplateView,
#                                 CreateView,UpdateView,DeleteView)


class CourseCreateView(CreateView):
    fields = '__all__'
    template_name = 'course/course_form.html'
    model = models.Course

    def get_success_url(self):
        return reverse('home')


class SubjectCreateView(CreateView):
    fields = ('name','marks')
    template_name = 'subject/subject_form.html'
    model = models.Subject

    def get_success_url(self):
        return reverse('home')


# class SubjectUpdateView(UpdateView):
#     fields = ('name','principle')
#     model = models.Subject
#
#
# class SubjectDeleteView(DeleteView):
#     model = models.Subject
#     success_url = reverse_lazy("basic_app:list")
#
#
# class CourseListView(ListView):
#     context_object_name = 'courses'
#     model = models.Course
#
#
# class CourseDetailView(DetailView):
#     context_object_name = 'course_detail'
#     model = models.Course
#     template_name = 'course_details.html'
#
#
#
# class CourseUpdateView(UpdateView):
#     fields = ('name','principle')
#     model = models.Course
#
#
# class CourseDeleteView(DeleteView):
#     model = models.Course
#     success_url = reverse_lazy("basic_app:list")
#
#
# class SubjectListView(ListView):
#     context_object_name = 'subjects'
#     model = models.Subject
#
#
# class SubjectDetailView(DetailView):
#     context_object_name = 'subject_detail'
#     model = models.Subject
#     template_name = 'subject_details.html'
#
