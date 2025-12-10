# accounts/urls.py
from django.urls import path
from .views import RegisterView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]


#    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NTk5MDgzMywiaWF0IjoxNzY1Mzg2MDMzLCJqdGkiOiI0NjY2ZWZkNjhiOTQ0ODE2ODY1Yzk4ZjIzMTJjZTkxOSIsInVzZXJfaWQiOiIzIn0.m0e7YHIvY1WqPukfgoXQwAgJ7jNuJ2TJdYR5mXXq940",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1Mzg3ODMzLCJpYXQiOjE3NjUzODYwMzMsImp0aSI6IjFjOGM1ODNhNmFkMTRjZTY5NzgwMjFlN2E1M2UwY2IxIiwidXNlcl9pZCI6IjMifQ.YTPP0gQNklqrZJrpb3pPlCa8x7ZwyBZbtMG-ESrGxwE