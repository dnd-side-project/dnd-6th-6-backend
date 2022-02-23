from django.urls import path
from houses import views


urlpatterns = [
    path("", views.create_house),
    path("invite", views.invite_member),
    path("invite/accept", views.accept_invite),
    path("members", views.get_members)
]
