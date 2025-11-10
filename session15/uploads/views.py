from rest_framework import generics, permissions, parsers, pagination, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


from .models import Upload
from .serializers import UploadSerializer

class UploadPagination(PageNumberPagination):
    page_size = 2

# Create your views here.
class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by('-created_at')
    serializer_class = UploadSerializer
    pagination_class = UploadPagination
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]





