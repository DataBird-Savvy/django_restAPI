from django.urls import path
from people_app.views import people_api,PeopleAPIView,PersonViewSet,RegisterAPI,LoginAPI
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from users.views import UserRegisterView,UserDetailView 


urlpatterns = [
    path('people/', people_api, name='people-api'),
    path('classpeople/', PeopleAPIView.as_view(), name='people-api-class'),
    path('register/', RegisterAPI.as_view(), name='register-api'),
    path('login/', LoginAPI.as_view(), name='login-api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwtregister/', UserRegisterView.as_view(), name='jwt-register-api'),
    path('jwtdetail/', UserDetailView.as_view(), name='jwt-user-detail-api'),
]


router=DefaultRouter()
router.register(r'person',PersonViewSet,basename='PersonViewSet')
urlpatterns +=router.urls