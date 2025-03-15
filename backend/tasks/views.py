from django.shortcuts import render, get_object_or_404
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
    if request.method == "POST":
        task_ids = request.POST.getlist("task_ids")
        new_status = request.POST.get("bulk_status")
        print(f">>>>>>>>>>>> {task_ids} {new_status}")
        if task_ids and new_status:
            Task.objects.filter(pk__in=task_ids).update(status=new_status)
            tasks = Task.objects.all()
            paginated = Paginator(tasks, 5)
            page_number = request.GET.get("page", 1)
            page = paginated.get_page(page_number)
            context = {
                "tasks": page,
                "status": Task.STATUS_CHOICES
            }
            return render(request, "partials/table.html", context)
        else:
            print("Invalid request NO MORE IDS")
            return HttpResponse("Invalid request: No task IDs or status provided", status=400)
    else:
        print("Invalid request")
        return HttpResponse("Invalid request: Must be POST", status=400)