from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver


# Define user roles as choices
class Role(models.TextChoices):
    READER = 'READER', _('Reader')
    JOURNALIST = 'JOURNALIST', _('Journalist')
    PUBLISHER = 'PUBLISHER', _('Publisher')

class User(AbstractUser):
    """
    Custom user model extended from Django's AbstractUser.
    Assigns a role and links to relevant groups.
    """

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.READER,
        help_text="Defines the role of the user: Reader, Journalist, or Editor."
    )

    # Reader-specific fields
    subscriptions_to_publishers = models.ManyToManyField(
        'Publisher',
        related_name='subscribed_readers',
        blank=True,
        help_text="Only applicable to readers. Subscriptions to publishers."
    )
    subscriptions_to_journalists = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='subscribed_by_readers',
        blank=True,
        help_text="Only applicable to readers. Subscriptions to journalists."
    )

    def save(self, *args, **kwargs):
        """
        Override save to assign users to their role-based group automatically.
        Also ensures irrelevant subscription fields are cleared.
        """
        super().save(*args, **kwargs)
        group, _ = Group.objects.get_or_create(name=self.role)
        self.groups.set([group])  # Set user's group based on role

        # Enforce one-role rule: clear unused fields
        if self.role == Role.JOURNALIST:
            self.subscriptions_to_publishers.clear()
            self.subscriptions_to_journalists.clear()
        elif self.role == Role.READER:
            pass  # Subscriptions remain usable
        else:
            self.subscriptions_to_publishers.clear()
            self.subscriptions_to_journalists.clear()

class Publisher(models.Model):
    """
    Represents a news publishing entity that can have multiple editors, journalists, and subscribers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='publisher_profile')
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='publisher_logos/', blank=True, null=True)

    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='editor_of_publishers',
        blank=True,
        help_text="Users with the Editor role."
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='journalist_of_publishers',
        blank=True,
        help_text="Users with the Journalist role."
    )

    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_publishers',
        blank=True,
        help_text="Users who subscribed to this publisher."
    )

    def __str__(self):
        return self.name

class Article(models.Model):
    """
    News article created by a journalist. May be published independently or under a publisher.
    Requires editor approval.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'JOURNALIST'})
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.SET_NULL,  
        null=True,                  
        blank=True,
        related_name='articles'
    )

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def is_independent(self):
        return self.publisher is None


class Newsletter(models.Model):
    """
    Newsletters created by journalists, optionally under a publisher.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newsletters'
    )

    def __str__(self):
        return f"Newsletter: {self.title}"

    def is_independent(self):
        return self.publisher is None

class JournalistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='journalist_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_journalist_profile(sender, instance, created, **kwargs):
    if created:
        JournalistProfile.objects.create(user=instance)
