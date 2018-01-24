from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from . import views
from .forms import LoginForm, ResetUserPasswordForm, SetUserPasswordForm, ChangeUserPasswordForm


app_name = "gambit"

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", views.Home.as_view(), name="home"),
    url(r"^profile/$", views.ViewProfile.as_view(), name="profile"),
    url(r"^password_change/$", auth_views.password_change, {"template_name": "gambit/password_change.html", 'password_change_form': ChangeUserPasswordForm},
        name="password_change"),
    url(r"^password_change_done/$", auth_views.password_change_done, {"template_name": "gambit/password_change_done.html"},
        name="password_change_done"),
    url(r"^update_profile/$", views.UpdateProfile.as_view(), name="update_profile"),
    url(r"^submission/(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89aAbB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})/$",
        views.ViewSubmission.as_view(), name="submission"),
    url(r"^submit/$", views.submit_form_upload, name="submit"),
    url(r"^update_submission/(?P<pk>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89aAbB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})/$",
        views.UpdateSubmission.as_view(), name="update_submission"),
    url(r"^new_review/(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89aAbB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})/$",
        views.CreateReview.as_view(), name="new_review"),
    url(r"^update_review/(?P<pk>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89aAbB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})/$",
        views.UpdateReview.as_view(), name="update_review"),
    url(r"^submissions/$", views.ListSubmission.as_view(), name="list_submissions"),
    url(r"^help/$", views.Help.as_view(), name="help"),
    url(r"^login/$", auth_views.login, {"template_name": "gambit/login.html", "redirect_authenticated_user": True, "authentication_form": LoginForm},
        name ="login"),
    url(r"^logout/$", auth_views.logout, {"next_page": "home"}, name ="logout"),
    url(r"^signup/$", views.signup, name="signup"),
    url(r"^password_reset/$", auth_views.password_reset, {"password_reset_form": ResetUserPasswordForm, "template_name": "gambit/password_reset_form.html",
        "email_template_name": "gambit/password_reset_email.html",
        "subject_template_name": "gambit/password_reset_subject.txt",}, name="password_reset"),
    url(r"^password_reset/done/$", auth_views.password_reset_done,
        {"template_name": "gambit/password_reset_done.html"}, name="password_reset_done"),
    url(r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.password_reset_confirm, {"template_name": "gambit/password_reset_confirm.html", "set_password_form": SetUserPasswordForm},
        name="password_reset_confirm",),
    url(r"^reset/done/$", auth_views.password_reset_complete, {"template_name": "gambit/password_reset_complete.html"},
        name="password_reset_complete"),
    url(r"^account_activation_sent/$", views.account_activation_sent, name="account_activation_sent"),
    url(r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.activate,
        name="activate"),
]

handler400 = views.BadRequest.as_view()
handler403 = views.PermissionDenied.as_view()
handler404 = views.PageNotFound.as_view()
handler500 = views.ServerError.as_view()

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
