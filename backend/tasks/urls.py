from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="task")

urlpatterns = [
    path("", views.TasksListView.as_view(), name="task_list"),
    path("update/<int:pk>", views.update_task, name="update_task"),
    path("delete/<int:pk>", views.delete_task, name="delete_task"),
    path("bulk-update/", views.bulk_update_tasks, name="bulk_update_tasks"),
    path("bulk-delete/", views.bulk_delete_tasks, name="bulk_delete_tasks"),
    
    path("api/", include(router.urls))
]
