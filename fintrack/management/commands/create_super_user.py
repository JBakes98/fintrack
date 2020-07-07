from django.core.management.base import BaseCommand
from fintrack_be.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email='joshbaker286.jb@gmail.com').exists():
            User.objects.create_superuser('joshbaker286.jb@gmail.com',
                                          'p1234567',
                                          first_name='Josh',
                                          last_name='Baker')
