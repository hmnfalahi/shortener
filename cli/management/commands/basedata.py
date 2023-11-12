from django.core.management.base import BaseCommand

from cli.management.commands.helpers import create_basedata


class Command(BaseCommand):
    help = """Generate BaseData"""

    def handle(self, *args, **options):
        create_basedata()
        print('Task Created Successfully')

