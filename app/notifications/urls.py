from django.urls import path

from notifications import views

urlpatterns = [
    path("", views.get_notifications),
    path("<int:pk>", views.check_notification)
]