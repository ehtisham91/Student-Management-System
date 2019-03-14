from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from sms.views import HomeView, search
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('search/', search, name='search'),

    path('student/', include("student.urls"), name='student'),
    path('marksheet/', include("result.urls"), name='result'),
    path('course/', include("course.urls"), name='course'),
    path('chart/', include("chart.urls"), name='chart'),

    path('login/', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
]
