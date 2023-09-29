import time

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("this is a test command running ....")
        time.sleep(5)
        print("test command done")
