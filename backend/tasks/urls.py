from django.urls import path
from . import views

urlpatterns = [
    path("", views.tasks_dashboard, name="task_list"),
    path("update/<int:pk>", views.update_task, name="update_task"),
    path("bulk-update/", views.bulk_update_tasks, name="bulk_update_tasks"),
]
