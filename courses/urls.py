from rest_framework.routers import SimpleRouter

from courses.views import CourseViewSet
from courses.apps import CoursesConfig


app_name = CoursesConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = []
urlpatterns += router.urls
