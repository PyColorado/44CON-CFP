import uuid
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    country = models.CharField(max_length=48)
    affiliation = models.CharField(max_length=32, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# During user signup, a linked profile object is tied to the generated user object
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    authors = models.TextField(blank=True)
    contact_email = models.EmailField()
    abstract = models.TextField(blank=True)
    conflicts = models.TextField(blank=True)
    file = models.FileField(upload_to="uploads/submissions/%Y/%m/%d/", blank=True)

    def __str__(self):
        return '{0!s}'.format(self.title)

    def get_reviews(self):
        return SubmissionReview.objects.filter(submission=self).order_by("submitted_on")

    def get_average_score(self):
        return SubmissionReview.objects.filter(submission=self).aggregate(models.Avg("submission_score"))["submission_score__avg"]

    def get_total_score(self):
        return SubmissionReview.objects.filter(submission=self).aggregate(models.Sum("submission_score"))["submission_score__sum"]


class SubmissionReview(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    expertise_score = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    submission_score = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.TextField(blank=True)

    def __str__(self):
        return '{0!s}'.format(self.uuid)


    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class ManagedContent(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class SubmissionDeadline(ManagedContent):
    date = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name = "Submission Deadline"
        verbose_name_plural = "Submission Deadline"


class FrontPage(ManagedContent):
    leading_paragraph = models.TextField()
    submission_paragraph = models.TextField()


    class Meta:
        verbose_name = "Front Page"
        verbose_name_plural = "Front Page"


class HelpPageItem(ManagedContent):
    title = models.CharField(max_length=64)
    content = models.TextField()


    class Meta:
        verbose_name = "Help Page"
        verbose_name_plural = "Help Page"
