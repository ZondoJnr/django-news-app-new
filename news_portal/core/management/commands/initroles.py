from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from core.models import Role

class Command(BaseCommand):
    help = "Initializes roles and assigns permissions to each group"

    def handle(self, *args, **kwargs):
        # Define permission sets
        view_perms = ['view_article', 'view_newsletter']
        edit_perms = view_perms + ['add_article', 'change_article', 'delete_article',
                                   'add_newsletter', 'change_newsletter', 'delete_newsletter']

        # Reader
        reader_group, _ = Group.objects.get_or_create(name=Role.READER)
        reader_group.permissions.set(Permission.objects.filter(codename__in=view_perms))

        # Journalist
        journalist_group, _ = Group.objects.get_or_create(name=Role.JOURNALIST)
        journalist_group.permissions.set(Permission.objects.filter(codename__in=edit_perms))

        # Editor
        editor_group, _ = Group.objects.get_or_create(name=Role.EDITOR)
        editor_group.permissions.set(Permission.objects.filter(codename__in=edit_perms))

        self.stdout.write(self.style.SUCCESS('Roles and permissions initialized.'))
