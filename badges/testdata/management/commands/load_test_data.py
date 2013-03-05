from django.core.management.base import BaseCommand, CommandError

from testdata.models import load_test_data

class Command(BaseCommand):
    args = '<data_file>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        load_test_data(args[0])
