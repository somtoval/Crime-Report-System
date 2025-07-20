from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    # ###########################################
    # User Routes
    # ###########################################
    path("dashboard/", views.dashboard, name="dashboard"),
    path("report/new/", views.file_report, name="file_report"),
    path("reports/my/", views.my_reports, name="my_reports"),
    path("reports/my/<uuid:report_id>/", views.report, name="view_report"),
    path("notifications/", views.notifications, name="notifications"),
    path("profile/settings/", views.profile_settings, name="profile_settings"),
    path("help/", views.help_support, name="help_support"),
]
