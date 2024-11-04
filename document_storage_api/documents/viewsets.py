from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        document = serializer.save()  # Save the document instance
        # Log the file URL or S3 key to verify it’s been uploaded
        print(f"Document saved with title: {document.title}")
        print(f"Document S3 key: {document.file.name}")
        print(f"Document URL: {document.file.url}")  # This URL is the S3 URL

    @swagger_auto_schema(responses={201: DocumentSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
