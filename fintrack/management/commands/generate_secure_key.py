from django.core.management import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    def handle(self, *args, **options):
        self.stdout.write('Running test...')
        generate_secure_key(self, options['mode'])
        self.stdout.write('done')


def generate_secure_key(self, mode):
    print(get_random_secret_key())
