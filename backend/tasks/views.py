from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task

def tasks_dashboard(request):
    tasks = Task.objects.all()
    paginated = Paginator(tasks, 5)
    page_number = request.GET.get("page", 1)
    page = paginated.get_page(page_number)
    context = {
        "tasks" : page,
        "status" : Task.STATUS_CHOICES
    }
    return render(request, "index.html", context)


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()
        return render(request, "partials/row.html", {"task": task, "status": Task.STATUS_CHOICES})
    
def bulk_update_tasks(request):
    if request.method != "POST":
        return HttpResponse("Invalid request: Must be POST", status=400)

    # Collect records ids in a list
    task_ids = request.POST.getlist("task_ids")
    # get the new status value
    new_status = request.POST.get("bulk_status")

    # Terminate if there are no selected ids or no status provided
    if not task_ids or not new_status:
        return HttpResponse("Invalid request: No task IDs or status provided", status=400)

    # Fetch all selected tasks
    all_tasks = Task.objects.filter(pk__in=task_ids)

    # Filter out tasks with "DONE" status if the new status is "DONE"
    if new_status is Task.DONE_STATUS:
        valid_tasks = all_tasks.exclude(status=Task.DONE_STATUS)
    else:
        valid_tasks = all_tasks

    # If the new status is "DONE", exclude tasks with "Not Started" status
    if new_status == Task.DONE_STATUS:
        valid_tasks = valid_tasks.exclude(status=Task.NOT_STARTED_STATUS)

    # Batch update the status of all valid tasks
    valid_tasks.update(status=new_status)

    if (len(all_tasks) != 5):
        all_tasks = Task.objects.all()
    paginated = Paginator(all_tasks, 5)
    page_number = request.GET.get("page", 1)
    page = paginated.get_page(page_number)
    context = {
        "tasks": page,
        "status": Task.STATUS_CHOICES
    }
    return render(request, "partials/table.html", context)