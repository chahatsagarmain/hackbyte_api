from django.urls import path
from .views import ChatView , ChatSessionView

urlpatterns = [
    path("chat",view=ChatView.as_view(),name="chat"),
    path("chatsession",view=ChatSessionView.as_view(),name="chat_session")
]