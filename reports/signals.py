from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CrimeCategory
from django.contrib.auth.models import User


categories = [
    "Theft",
    "Burglary",
    "Assault",
    "Robbery",
    "Vandalism",
    "Fraud",
    "Cybercrime",
    "Homicide",
    "Arson",
    "Kidnapping",
]


@receiver(post_migrate)
def populate_database(sender, **kwargs):
    for category in categories:
        if not CrimeCategory.objects.filter(name=category).exists():
            CrimeCategory.objects.create(name=category)
    print("Crime categories populated.")


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if User.objects.filter(username="admin") or User.objects.filter(
        email="admin@gmail.com"
    ):
        return
    User.objects.create_superuser(
        email="admin@gmail.com", username="admin", password="admin123"
    )
    print("Admin account created!")
