from .models import CustomUser
from .serializers import LoginSerializer


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
