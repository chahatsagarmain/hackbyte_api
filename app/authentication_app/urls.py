from django.urls import path
from .views import LoginAPIView, RegisterAPIView, TestAPIView , LogoutAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('test', TestAPIView.as_view(), name='test'),
    path('logout', LogoutAPIView.as_view() , name = "logout")
]