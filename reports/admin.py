from django.contrib import admin
from django.contrib.auth.models import User
from .models import CrimeReport, Case, Suspect, Victim, CrimeCategory, Evidence


class CrimeReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter", "location", "crime_type", "reported_at")
    list_filter = ("crime_type", "reported_at")  # Add filters to the sidebar
    search_fields = ("location", "description", "reporter__username")  # Enable search
    ordering = ("-reported_at",)  # Default ordering
    fieldsets = (
        ("Reporter Information", {"fields": ("reporter",)}),
        (
            "Crime Details",
            {"fields": ("crime_type", "location", "crime_time", "description")},
        ),
        ("Date Reported", {"fields": ("reported_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ("reported_at",)


class SuspectInline(
    admin.TabularInline
):  # Or admin.StackedInline for a different layout
    model = Suspect
    extra = 1  # Number of empty forms to display


class VictimInline(admin.TabularInline):
    model = Victim
    extra = 1


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1


class CaseAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "status", "assigned_officer")
    list_filter = ("status", "assigned_officer")
    search_fields = ("report__location", "notes", "assigned_officer__username")
    inlines = [SuspectInline, VictimInline, EvidenceInline]


class SuspectAdmin(admin.ModelAdmin):
    list_display = ("id", "case", "name")
    list_filter = ("case",)
    search_fields = ("name", "description")


class VictimAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "name")
    list_filter = ("report",)
    search_fields = ("name",)


class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("id", "case", "collected_at")
    list_filter = ("case",)
    search_fields = ("description",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


admin.site.register(CrimeReport, CrimeReportAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Suspect, SuspectAdmin)
admin.site.register(Victim, VictimAdmin)
admin.site.register(Evidence, EvidenceAdmin)
admin.site.register(CrimeCategory, CategoryAdmin)
