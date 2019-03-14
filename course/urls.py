from django.urls import path
from course import views

app_name = 'course'
urlpatterns = [
    path('create/subject/',views.SubjectCreateView.as_view(),name='create_subject'),
    path('create/',views.CourseCreateView.as_view(),name='create'),
]
