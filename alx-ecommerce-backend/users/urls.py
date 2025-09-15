from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
