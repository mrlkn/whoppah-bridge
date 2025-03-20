from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User

class Command(BaseCommand):
    help = 'Create an admin user non-interactively'

    def handle(self, *args, **options):
        self.stdout.write('Creating admin user...')
        
        if not User.objects.filter(email='admin@whoppahbridge.com').exists():
            user = User.objects.create_superuser(
                email='admin@whoppahbridge.com',
                password='AdminPassword123!',
                first_name='Admin',
                last_name='User',
                user_type=User.Types.ADMIN
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists, no changes made.'))
