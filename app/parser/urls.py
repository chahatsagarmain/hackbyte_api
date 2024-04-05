from django.urls import path
from .views import UploadView , ParserView

urlpatterns = [
    path('file',view=UploadView.as_view(),name="file uploading"),
    path('parser',view=ParserView.as_view(),name="parse_pdf")
]
