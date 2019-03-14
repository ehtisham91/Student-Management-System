from django.conf.urls import url
from course import views

app_name='course'
urlpatterns = [
    url(r'^create/subject/$',views.SubjectCreateView.as_view(),name='create_subject'),
    url(r'^create/$',views.CourseCreateView.as_view(),name='create'),
    # url(r'^(?P<pk>\d+)/$',views.CourseDetailView.as_view(),name='detail'),
    # url(r'^update/(?P<pk>\d+)/$',views.CourseUpdateView.as_view(),name='update'),
    # url(r'^delete/(?P<pk>\d+)/$',views.CourseDeleteView.as_view(),name='delete'),
]
