from django.urls import path
from . import views

app_name = 'result'
urlpatterns = [
    path('<int:pk>/',views.MarkSheetDetailView.as_view(), name='detail'),
    path('create/',views.MarkSheetCreateView.as_view(), name='create'),
    path('ajax/load-cities/', views.load_courses, name='ajax_load_courses'),
    path('pdf_report/', views.Report.as_view(), name='report'),
    path('detail/<int:pk>/$',views.edit_marksheet_detail, name='marksheet_detail')

]
