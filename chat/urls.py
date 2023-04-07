from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from chat.views import (ThreadListCreateView, ThreadUpdateDeleteView, MessageListCreateView,
                        MessageReadView, UserThreadListView, GetUnreadMessageView,
                        UserRegisterView)


urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='user_register'),
    path('users/<int:pk>/messages/', GetUnreadMessageView.as_view(), name='messages_unread'),
    path('threads/', ThreadListCreateView.as_view(), name='threads_list_create'),
    path('threads/user/<int:pk>/', UserThreadListView.as_view(), name='user_threads'),
    path('threads/<int:pk>/', ThreadUpdateDeleteView.as_view(), name='threads_update_delete'),
    path('threads/<int:thread_id>/messages/', MessageListCreateView.as_view(), name='messages_list_create'),
    path('threads/<int:thread_id>/messages/<int:pk>/', MessageReadView.as_view(), name='message_read'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
