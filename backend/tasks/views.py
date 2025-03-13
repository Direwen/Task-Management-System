from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import TaskForm
from .models import Task

def tasks_dashboard(request):
    tasks = Task.objects.all()
    paginated = Paginator(tasks, 5)
    page_number = request.GET.get("page")
    page = paginated.get_page(page_number)
    context = {
        "tasks" : page,
    }
    return render(request, "index.html", context)
        
