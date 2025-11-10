import hashlib
import os.path
import re

import magic
from rest_framework import serializers

from .models import Upload


SAFE_EXTS = {'.jpg', '.jpeg', '.png', '.webp','.pdf'}
MAX_SIZE = 1024*1024*10

def sanitize_filename(name:str) -> str:
    name = os.path.basename(name)
    name = re.sub(r'[^A-Za-z0-9\-._]+]', '_', name)
    return name[:200]

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'
        read_only_fields = ['original_name','mime_type', 'extension', 'size_bytes', 'sha256',
                            'is_image', 'is_valid', 'created_at']

    def validate_file(self,f):
        if f.size > MAX_SIZE:
            raise serializers.ValidationError('File size is too big, max allowed size is 10 MB')

        original_name = getattr(f,'name','upload.bin')
        ext = os.path.splitext(original_name)[1].lower()
        if ext not in SAFE_EXTS:
            raise serializers.ValidationError('Unsupported file extension')

        head = f.read(4096)
        f.seek(0)
        mime = magic.from_buffer(head, mime=True) or ""
        allowed_mimes = {
            'image/jpeg', 'image/jpeg', 'image/png', 'image/webp', 'application/pdf',
        }
        if mime not in allowed_mimes:
            raise serializers.ValidationError('Unsupported file type')
        if ext == '.pdf' and not head.startswith(b'%PDF'):
            raise serializers.ValidationError('Unsupported PDF file')
        return f

    def create(self, validated_data):
        f = validated_data['file']

        #compute metadata
        original_name = sanitize_filename(getattr(f,'name','upload.bin'))
        ext = os.path.splitext(original_name)[1].lower()

        #compute sha256 incrementally
        sha = hashlib.sha256()
        for chunk in f.chunks():
            sha.update(chunk)
        sha256 = sha.hexdigest()

        #Reset pointer so Django can save file content
        f.seek(0)

        # Detect MIME again (safe)
        head = f.read(4096)
        f.seek(0)
        mime = magic.from_buffer(head, mime=True) or ""
        is_image = mime.startswith('image/')

        instance = Upload.objects.create(
            file=f,
            original_name=original_name,
            mime_type=mime,
            extension=ext,
            size_bytes=f.size,
            sha256=sha256,
            is_image=is_image,
        )
        return instance