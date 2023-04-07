from django.urls import path
from chat.views import (ThreadListCreateView, ThreadUpdateDeleteView, MessageListCreateView,
                        MessageReadView, UserThreadListView, GetUnreadMessageView,
                        UserRegisterView)


urlpatterns = [
    path('threads/', ThreadListCreateView.as_view(), name='threads_list_create'),
    path('threads/user/<int:pk>/', UserThreadListView.as_view(), name='threads_user'),
    path('threads/<int:pk>/', ThreadUpdateDeleteView.as_view(), name='thread_update_delete'),
    path('threads/<int:thread_id>/messages/', MessageListCreateView.as_view(), name='messages_list_create'),
    path('threads/<int:thread_id>/messages/<int:pk>/', MessageReadView.as_view(), name='message_read'),
    path('users/<int:pk>/messages/', GetUnreadMessageView.as_view(), name='get_messages_unread'),
    path('users/register/', UserRegisterView.as_view(), name='user_register'),
]
