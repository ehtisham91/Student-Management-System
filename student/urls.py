from django.urls import path
from student import views

app_name = 'student'
urlpatterns = [
    # path('<int:pk>/', views.StudentDetailView.as_view(), name='detail'),
    path('create/', views.StudentCreateView.as_view(), name='create'),
]
