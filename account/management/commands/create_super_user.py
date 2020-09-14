from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not UserModel.objects.filter(email='joshbaker286.jb@gmail.com').exists():
            UserModel.objects.create_superuser('joshbaker286.jb@gmail.com',
                                          'p1234567',
                                          first_name='Josh',
                                          last_name='Baker')
