from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer

# تسجيل مستخدم جديد (Signup) → أي شخص يقدر يسجل
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # <--- صحح هنا

# عرض بروفايل المستخدم → لازم يكون مسجل دخول
class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # <--- صح

    def get_object(self):
        return self.request.user


