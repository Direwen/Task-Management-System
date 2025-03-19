from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.generic import ListView
from .forms import TaskForm
from .models import Task

def get_paginated_tasks(request, tasks=None):
    """Helper function to paginate tasks and build context."""
    # Use provided tasks or fetch all if None
    tasks = tasks if tasks is not None else Task.objects.all()
    paginated = Paginator(tasks, 5)
    page = paginated.get_page(request.GET.get("page", 1))
    return {
        "tasks": page,
        "status": Task.STATUS_CHOICES
    }

class TasksListView(ListView):
    model = Task
    template_name = "index.html"
    context_object_name = "tasks"
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title", "").strip()
        print(f"Searching for: {title}")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = Task.STATUS_CHOICES
        context["search_query"] = self.request.GET.get("title", "")
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # If it's an HTMX request and not targeting a specific element, return only the table
        if request.htmx:
            return render(request, "partials/table.html", self.get_context_data())
        return response

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()
        return render(request, "partials/row.html", {"task": task, "status": Task.STATUS_CHOICES})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        context = get_paginated_tasks(request)
        return render(request, "partials/table.html", context)

def bulk_update_tasks(request):
    if request.method != "POST":
        return HttpResponse("Invalid request: Must be POST", status=400)

    task_ids = request.POST.getlist("task_ids")
    new_status = request.POST.get("bulk_status")
    if not task_ids or not new_status:
        return HttpResponse("Invalid request: No task IDs or status provided", status=400)

    all_tasks = Task.objects.filter(pk__in=task_ids)
    if new_status is Task.DONE_STATUS:
        valid_tasks = all_tasks.exclude(status=Task.DONE_STATUS)
    else:
        valid_tasks = all_tasks

    if new_status == Task.DONE_STATUS:
        valid_tasks = valid_tasks.exclude(status=Task.NOT_STARTED_STATUS)

    valid_tasks.update(status=new_status)
    
    view = TasksListView()
    #To access pagination and query parameters
    view.setup(request)
    view.object_list = view.get_queryset()
    context = view.get_context_data()
    return render(request, "partials/table.html", context)

def bulk_delete_tasks(request):
    if request.method != "POST":
        return HttpResponse("Invalid request: Must be POST", status=400)

    task_ids = request.POST.getlist("task_ids")
    if not task_ids:
        return HttpResponse("Invalid request: No task IDs", status=400)

    Task.objects.filter(pk__in=task_ids).delete()
    
    view = TasksListView()
    #To access pagination and query parameters
    view.setup(request)
    view.object_list = view.get_queryset()
    context = view.get_context_data()
    return render(request, "partials/table.html", context)