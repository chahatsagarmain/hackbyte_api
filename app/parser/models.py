from django.db import models
from uuid import uuid4
from authentication_app.models import CustomUser

class PDF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id' , related_name='pdfs')
    file_url = models.URLField(blank=True)