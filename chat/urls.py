from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from chat.views import (ThreadListCreateView, ThreadUpdateDeleteView, MessageListCreateView,
                        MessageReadView, UserThreadListView, GetUnreadMessageView,
                        UserRegisterView)


urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='user_register'),  # User Register
    path('users/<int:pk>/messages/', GetUnreadMessageView.as_view(), name='messages_unread'),  # Unread Messages by User Id
    path('threads/', ThreadListCreateView.as_view(), name='threads_list_create'),  # Get or Create Threads
    path('threads/user/<int:pk>/', UserThreadListView.as_view(), name='user_threads'),  # Get Thread by User Id
    path('threads/<int:pk>/', ThreadUpdateDeleteView.as_view(), name='threads_update_delete'),  # Update or Delete Thread
    path('threads/<int:thread_id>/messages/', MessageListCreateView.as_view(), name='messages_list_create'),  # Get Thread Messages or Create if you Participant
    path('threads/<int:thread_id>/messages/<int:pk>/', MessageReadView.as_view(), name='message_read'),  # Read Message if you Participant(not sender)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT-Auth
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify JWT token
]
