from django.urls import path, include
from .views import  chart, chart_data, course_wise_performance

urlpatterns = [
    path(r'', chart, name='chart'),
    path('json-chart/data/', chart_data, name='chart_data'),
    path('<int:pk>/', course_wise_performance, name='course_chart'),
]
