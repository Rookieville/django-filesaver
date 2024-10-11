from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(source='UploadFiles', write_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at']

