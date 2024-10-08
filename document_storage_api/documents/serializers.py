from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(source='UploadFiles', write_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 's3_key', 'uploaded_at']
        read_only_fields = ['id', 's3_key', 'uploaded_at']
