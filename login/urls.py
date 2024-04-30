from django.urls import path

from . import views
from .views import google_login
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = "login"

urlpatterns = [
    path("", views.welcome_page, name="welcome"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("<int:report_id>/submission", views.see_submission, name="submission"),
    path('google-login/', google_login, name='google_login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('<int:report_id>/resolve_report', views.resolve_report, name='resolve_report'),
    path('update_notes/', views.update_notes, name='update_notes'),
    path('view_reports/', views.view_reports, name='view_reports'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)