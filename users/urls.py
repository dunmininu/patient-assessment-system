from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()
router.register(r"register", UserViewSet, basename="user")

urlpatterns = router.urls
