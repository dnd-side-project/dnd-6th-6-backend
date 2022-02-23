"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from chores.views import ChoreViewSet, RepeatChoreViewSet, get_categories
from comments.views import CommentChoreViewSet, CommentRepeatChoreViewSet
from favor.views import FavorViewSet
from feedbacks.views import FeedbackViewSet
from notices.views import NoticeViewSet

router = routers.DefaultRouter()
router.register(r"houses/(?P<house_id>\d+)/chores", ChoreViewSet)
router.register(r"houses/(?P<house_id>\d+)/repeat-chores", RepeatChoreViewSet)
router.register(r"houses/(?P<house_id>\d+)/notices", NoticeViewSet)
router.register(r"chores/(?P<chore_id>\d+)/feedbacks", FeedbackViewSet)
router.register(r"chores/(?P<chore_id>\d+)/comments", CommentChoreViewSet)
router.register(r"chores/(?P<chore_id>\d+)/favor", FavorViewSet)
router.register(
    r"repeat-chores/(?P<repeat_chore_id>\d+)/comments", CommentRepeatChoreViewSet
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("houses/", include("houses.urls")),
    path("notifications/", include("notifications.urls")),
    path("users/", include("users.urls")),
    path("categories", get_categories)
]


urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
