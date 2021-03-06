import csv

from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponse
from django.template import defaultfilters
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import (Profile, Submission, SubmissionReview, FrontPage, SubmissionDeadline, RegistrationStatus,
    HelpPageItem)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        '_username',
        '_last_login',
    )
    search_fields = [
        'name',
        'user__username',
    ]

    # Renders the related username as a link to the edit page for the actual user object
    def _username(self, obj):
        link_to_user_object = reverse('admin:auth_user_change', args=(obj.user.id,))
        return mark_safe(f"<a href='{link_to_user_object}'>{obj.user.username}</a>")
    _username.short_description = "User"

    def _last_login(self, obj):
        return obj.user.last_login
    _last_login.short_description = "Last login"


admin.site.register(Profile, ProfileAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        '_username',
        '_timestamp',
        '_score',
    )
    list_filter = (
        'user__username',
        'submitted_on',
    )
    readonly_fields = ('file_hash',)
    actions = ['_export_to_csv']

    # Adds button in top right which will open the submission on the live site
    def view_on_site(self, obj):
        return reverse("submission", args=(obj.uuid,))

    # Renders the related username as a link to the edit page for the actual user object
    def _username(self, obj):
        link_to_user_object = reverse("admin:auth_user_change", args=(obj.user.id,))
        return mark_safe(f"<a href='{link_to_user_object}'>{obj.user.username}</a>")
    _username.short_description = "User"

    # ISO 8601 date formatting or GTFO
    def _timestamp(self, obj):
        return defaultfilters.date(obj.submitted_on, "Y-m-d H:i")

    def _score(self, obj):
        return obj.get_average_score()

    def _export_to_csv(self, request, queryset):
        """I apologise for this horrendous method."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=cfp-submissions.csv"
        writer = csv.writer(response)
        writer.writerow(['Title', 'Authors', 'Contact', 'Submitted On', 'Score', 'Submitter', 'Submitter Email', 'Country',])
        submissions = queryset.values_list('title', 'authors', 'contact_email', 'submitted_on',)
        for index, submission in enumerate(submissions):
            # submission is iterated out to create a list instead of a tuple so that the score can be appended
            # I was lazy with this and there's probably a far more elegant way to do it
            submission = [field for field in submission]
            submission.append(queryset[index].get_average_score())
            submission.append(queryset[index].user.profile.name)
            submission.append(queryset[index].user.email)
            submission.append(queryset[index].user.profile.country)
            writer.writerow(submission)
        return response
    _export_to_csv.short_description = "Export to CSV"


admin.site.register(Submission, SubmissionAdmin)


class SubmissionReviewAdmin(admin.ModelAdmin):
    list_display = (
        '_submission',
        '_reviewer',
        'submitted_on',
        '_uuid_snip',
    )
    list_filter = (
        'user__username',
        'submitted_on',
    )
    actions = ['_export_to_csv']

    # Adds button in top right which will open the related submission on the live site
    def view_on_site(self, obj):
        return reverse("submission", args=(obj.submission.uuid,))

    def _submission(self, obj):
        return obj.submission.title

    def _reviewer(self, obj):
        return obj.user.username

    # Print the stripped hexadecimal of the object UUID for simple reference
    # Provides no functional benefit but is useful for debugging
    # Can be removed completely in production environment
    def _uuid_snip(self, obj):
        return obj.uuid.hex
    _uuid_snip.short_description = "UUID"

    def _export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=cfp-review-comments.csv"
        writer = csv.writer(response)
        writer.writerow(['Reviewer', 'Comments', 'Submission Title'])
        reviews = queryset.values_list('user__profile__name', 'comments', 'submission__title',)
        for review in reviews:
            writer.writerow(review)
        return response
    _export_to_csv.short_description = "Export to CSV"


admin.site.register(SubmissionReview, SubmissionReviewAdmin)


class FrontPageAdmin(admin.ModelAdmin):
    # This model is naively used to control the content display on the front page of the website
    # In later versions, this will be superceded by a content management system accessed through the website
    list_display = ('name',)

    def has_add_permission(self, *args, **kwargs):
        return not FrontPage.objects.exists()


admin.site.register(FrontPage, FrontPageAdmin)


class SubmissionDeadlineAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, *args, **kwargs):
        return not SubmissionDeadline.objects.exists()


admin.site.register(SubmissionDeadline, SubmissionDeadlineAdmin)


class RegistrationStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, *args, **kwargs):
        return not RegistrationStatus.objects.exists()


admin.site.register(RegistrationStatus, RegistrationStatusAdmin)


class HelpPageItemAdmin(admin.ModelAdmin):
    # This model is naively used to control the content display on the help page of the website
    # In later versions, this will be superceded by a content management system accessed through the website
    list_display = (
        'name',
        'id',
    )


admin.site.register(HelpPageItem, HelpPageItemAdmin)
