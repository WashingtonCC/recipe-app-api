"""
Django command to wait for the db to be available
"""
from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError

# django automatically detects this as a management command
# because of the folder structure


class Command(BaseCommand):
    """Django command to wait for db."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(
                    databases=["default"]
                )  # if we call this and the db is not ready,
                # it throws an exception
                # (the psycop one or the django op. error one)
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
