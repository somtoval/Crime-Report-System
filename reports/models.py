from django.db import models
from django.contrib.auth.models import User
import uuid


class CrimeReport(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    crime_type = models.CharField(max_length=100)
    crime_type = models.ForeignKey(
        "CrimeCategory", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    crime_time = models.DateTimeField()

    def __str__(self):
        return f"Report at {self.location} on {self.crime_time} by {self.reporter.username}"


class Case(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    report = models.OneToOneField(CrimeReport, on_delete=models.CASCADE)
    assigned_officer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_cases",
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("new", "New"),
            ("assigned", "Assigned"),
            ("investigating", "Investigating"),
            ("closed", "Closed"),
        ],
        default="new",
    )
    opened_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Case for Report ID: {self.report.id} - Status: {self.get_status_display()}"


class Suspect(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="suspects")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Add other relevant fields like date of birth, address, etc.

    def __str__(self):
        return self.name


class Victim(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    report = models.ForeignKey(
        CrimeReport,
        on_delete=models.CASCADE,
        related_name="victims",
        null=True,
        blank=True,
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="victims",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    # Add other relevant fields

    def __str__(self):
        return self.name


class Evidence(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="evidence")
    description = models.TextField()
    collected_at = models.DateTimeField(auto_now_add=True)
    # You might also want to store the actual evidence file or a link to it

    def __str__(self):
        return self.description[:50] + "..."


class CrimeCategory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
