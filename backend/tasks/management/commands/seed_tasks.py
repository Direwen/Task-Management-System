from django.core.management.base import BaseCommand
from tasks.models import Task
from django.contrib.auth.models import User
import random
from faker import Faker

class Command(BaseCommand):
    help = "Populates the database with a large number of tasks for testing bulk operations and pagination."

    def add_arguments(self, parser):
        # Optional argument for number of tasks
        parser.add_argument(
            "--count",
            type=int,
            default=500,
            help="Number of tasks to create (default: 500)",
        )

    def handle(self, *args, **options):
        # Get the count from arguments
        task_count = options["count"]

        # Check for admin user
        try:
            admin = User.objects.get(pk=1)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Superuser with pk=1 does not exist. Create one first.'))
            return

        # Initialize Faker for realistic data
        fake = Faker()

        # Define possible statuses
        statuses = [Task.NOT_STARTED_STATUS, Task.IN_PROGRESS_STATUS, Task.DONE_STATUS]

        # Generate tasks
        tasks = []
        for i in range(task_count):
            task = Task(
                user=admin,
                title=fake.sentence(nb_words=3).strip(".").lower(),  # e.g., "write project report"
                description=fake.text(max_nb_chars=100) if random.random() > 0.3 else "",  # 70% have descriptions
                status=random.choice(statuses),
            )
            tasks.append(task)

        # Bulk create tasks for efficiency
        Task.objects.bulk_create(tasks, batch_size=100)

        # Success message
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {task_count} tasks for user '{admin.username}'.")
        )