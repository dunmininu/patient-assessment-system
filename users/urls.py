from rest_framework.routers import DefaultRouter

from users.views import AuthenticationViewset, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"register", AuthenticationViewset, basename="auth")

urlpatterns = router.urls
