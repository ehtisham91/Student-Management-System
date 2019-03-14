from student.models import Student
from django.shortcuts import render
from django.db.models import Count, Q
from course.models import Course, Subject
from django.views.generic import TemplateView


def search(request):
    query = request.GET.get("q")
    if query:
        queryset_list = Student.objects.all().filter(
            Q(name__icontains=query) |
            Q(registrationNo__icontains=query)
        ).distinct()
        return render(request, "student/student_list.html", {'query_list':queryset_list})


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['students'] = Student.objects.all()
        context['courses'] = Course.objects.all()
        return context


