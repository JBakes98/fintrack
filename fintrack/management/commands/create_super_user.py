from django.core.management.base import BaseCommand
from fintrack_be.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email='joshbaker286.jb@gmail.com').exists():
            User.objects.create_superuser('joshbaker286.jb@gmail.com',
                                          'Bakercorp2861731',
                                          first_name='Josh',
                                          last_name='Baker')
