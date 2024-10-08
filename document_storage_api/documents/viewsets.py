from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    
    @swagger_auto_schema(
        operation_description="Upload a new document",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Successfully uploaded",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'isSuccess': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indicates if the upload was successful"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Success message")
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'isSuccess': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indicates if the upload failed"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                        'errors': openapi.Schema(type=openapi.TYPE_OBJECT, description="Detailed error information")
                    }
                )
            )
        }
    )
    def create(self, request, *args, **kwargs):
        file_serializer = DocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            # file_serializer.save()
            print(file_serializer.validated_data)
            return Response({
                'isSuccess': True,
                'message': 'File uploaded successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'isSuccess': False,
                'message': 'File upload failed',
                'errors': file_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            # Log the error here if needed
            raise Exception("Failed to save document: " + str(e))