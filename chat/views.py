from rest_framework import generics, status
from rest_framework.response import Response

from django.contrib.auth.models import User

from chat.models import Thread, Message
from chat.serializers import ThreadSerializer, MessageSerializer, UserRegisterSerializer


class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Thread.objects.filter(participants=user)
        else:
            return Thread.objects.all()


class ThreadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class UserThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer

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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id)


class MessageReadView(generics.RetrieveDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        message = self.get_object()
        if message.sender != request.user:
            message.is_read = True
            message.save()
        serialize_obj = self.get_serializer(message)
        return Response(serialize_obj.data)


class GetUnreadMessageView(generics.ListAPIView):
    serializer_class = MessageSerializer

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
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

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
