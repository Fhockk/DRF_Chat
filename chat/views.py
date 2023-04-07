from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User

from chat.models import Thread, Message
from chat.serializers import ThreadSerializer, MessageSerializer, UserRegisterSerializer


class ThreadListCreateView(generics.ListCreateAPIView):
    """
    GET the list of Threads for requested user;
    CREATE Thread
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user)


class ThreadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Thread by id
    UPDATE Thread by id
    Delete Thread by id
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated, )


class UserThreadListView(generics.ListAPIView):
    """
    GET Threads by User id
    """
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, **kwargs):
        pk = kwargs.get('pk', None)

        if pk is not None:
            instance = User.objects.get(pk=pk)
            if instance:
                return Thread.objects.filter(participants=instance)
            else:
                return Thread.objects.none()
        else:
            return Thread.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(**kwargs)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid pk or object does not exist"})


class MessageListCreateView(generics.ListCreateAPIView):
    """
    GET Messages of thread by id(thread)
    CREATE Message of thread by id(thread) IF you are participant of this Thread
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id)


class MessageReadView(generics.RetrieveDestroyAPIView):
    """
    GET Message of Thread by id(thread) and id(message) and READ it if you are
    participant of this Thread and NOT A SENDER
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        message = self.get_object()
        if message.sender != request.user:
            message.is_read = True
            message.save()
        serialize_obj = self.get_serializer(message)
        return Response(serialize_obj.data)


class GetUnreadMessageView(generics.ListAPIView):
    """
    GET Unread Messages from all Threads by id(User)
    """
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, **kwargs):
        pk = kwargs.get('pk', None)

        if pk is not None:
            instance = User.objects.get(pk=pk)
            if instance:
                return Message.objects.filter(thread__participants=instance, is_read=False).exclude(sender=instance)
            else:
                Message.objects.none()
        else:
            return Message.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(**kwargs)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid pk or object does not exist"})


class UserRegisterView(generics.CreateAPIView):
    """
    CREATE USER
    {
        "username":"text" (unique)
        "email":"someemail@mail.com";
        "password":"123";
        "password2":"123"
    }
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
