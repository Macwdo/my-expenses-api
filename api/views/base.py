# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication


class BaseModelViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    
