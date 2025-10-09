from django.core.management.base import BaseCommand
import os
from accounts.models import User, Roles
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Seeds the admin account, roles, and gender options"

    def handle(self, *args, **kwargs):
        admin_username = os.getenv("DJANGO_ADMIN_USERNAME")
        admin_email = os.getenv("DJANGO_ADMIN_EMAIL")
        admin_password = os.getenv("DJANGO_ADMIN_PASSWORD")
        admin_role = Roles.objects.get(name="Admin")
        if not User.objects.filter(username=admin_username).exists():
            usr = User.objects.create(
                username=admin_username,
                email=admin_email,
                role=admin_role,
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )
            usr.set_password(admin_password)
            usr.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin account {admin_username} created successfully."
                )
            )
        else:
            self.stdout.write(self.style.WARNING("Admin account already exists."))

        self.stdout.write(self.style.SUCCESS("running periodic task setup..."))
        interval, _ = IntervalSchedule.objects.update_or_create(
            every=15,
            period=IntervalSchedule.MINUTES,
        )
        

        PeriodicTask.objects.update_or_create(
            name='fetch-otrs-every-5-min',
            defaults={'interval': interval, 'task': 'agents.tasks.sync_database', 'enabled': True},
        )