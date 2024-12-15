from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
    LessonDestroyApiView, SubscriptionAPIView
)
from courses.apps import CoursesConfig


app_name = CoursesConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('lessons/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    path('lessons/', LessonListApiView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson_delete'),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription-manage')
]
urlpatterns += router.urls
