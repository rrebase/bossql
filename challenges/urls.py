from django.urls import path

from . import views


app_name = 'challenges'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.TopicDetailView.as_view(), name="topic_detail"),
    path("<int:pk>/admin-source-tables/", views.AdminTopicSourceTablesView.as_view(), name="admin_source_tables"),
    path("check-attempt/", views.CheckAttemptEndpoint.as_view(), name="check_attempt"),
]
