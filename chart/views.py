import json
from .forms import StudentForm
from django.shortcuts import render
from student.models import Student
from django.db.models import Count, Q
from result.models import MarkSheet
from django.http import JsonResponse
from course.models import Course, Subject
from django.views.generic import TemplateView


# bar chart filter on student
def chart(request):
    form = StudentForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data['name']
            dataset = MarkSheet.objects.filter(student=name)
            #There can be multiple courses against single user
            chart_list = list()
            for chart in dataset:
                chart_list.append(create_chart(chart))
            message = ""
            if dataset.count() == 0:
                message = "Nothing to show. Student you've selected, doesn't has any marksheet record"
            return render(request, 'course_wise_chart.html', {'chart_list': chart_list, 'msg': message})
    return render(request, 'charts.html', {'form': form})


# returns json data
def chart_data(request):
    dataset = Course.objects.values('title') \
        .annotate(students_count=Count('students')) \
        .order_by('title')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Pie – Students per course'},
        'series': [{
            'name': 'Courses',
            'data': list(map(lambda row: {'name': row['title'], 'y': row['students_count']}, dataset))
        }]
    }
    return JsonResponse(chart)


# creates chart according to data passed with parameter and returns data in json format
def create_chart(dataset):
    categories = list()
    students_obtained_marks = list()

    for cat in dataset.detail.all():
        categories.append(cat.subject)
        students_obtained_marks.append(cat.obtained_marks)

    students_series = {
        'name': 'Student Obtained Marks',
        'data': students_obtained_marks,
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Students marks in subject in {}'.format(dataset.course)},
        'xAxis': {'categories': categories},
        'yAxis': {
            'title': {
                'text': 'Marks'
            }
        },
        'series': [students_series]
    }
    dump = json.dumps(chart)
    return dump


def course_wise_performance(request, pk):
    obj = Student.objects.get(registrationNo=pk)
    dataset = MarkSheet.objects.filter(student=obj)
    chart_list = list()
    for chart in dataset:
        chart_list.append(create_chart(chart))
    return render(request, 'course_wise_chart.html', {'chart_list': chart_list})