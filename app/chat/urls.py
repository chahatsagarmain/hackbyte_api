from django.urls import path
from .views import ChatView , ChatSessionView , GetSession

urlpatterns = [
    path("chat",view=ChatView.as_view(),name="chat"),
    path("chatsession",view=ChatSessionView.as_view(),name="chat_session"),
    path("session",view=GetSession.as_view())
]