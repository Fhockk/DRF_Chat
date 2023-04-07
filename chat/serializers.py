from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from chat.models import Thread, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User
    """
    class Meta:
        model = User
        fields = ('id', 'username')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message
    """
    class Meta:
        model = Message
        fields = ('id', 'text', 'thread', 'sender', 'is_read', 'created')
        read_only_fields = ('id', 'thread', 'created', 'sender')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sender'] = request.user
        thread_id = request.parser_context.get('kwargs').get('thread_id')
        thread = get_object_or_404(Thread, id=thread_id)
        if validated_data['sender'] not in thread.participants.all():
            raise serializers.ValidationError("You're not the member of this thread")
        validated_data['thread'] = thread
        return super(MessageSerializer, self).create(validated_data)


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for Thread
    """
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ('id', 'participants', 'created', 'updated', 'last_message')

    def create(self, validated_data):
        valid_participants = validated_data.get('participants')
        if len(valid_participants) != 2:
            raise serializers.ValidationError("The thread can only have 2 participants")
        thread = Thread.objects.filter(participants=valid_participants[0]).filter(participants=valid_participants[1]).first()
        if not thread:
            thread = Thread.objects.create()
            thread.participants.set(valid_participants)
            thread.save()
        return thread

    @staticmethod
    def get_last_message(obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for USER REGISTRATION VIEW
    """
    email = serializers.CharField(required=True, max_length=64)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Password does not match'})
        user.set_password(password)
        user.save()
        return user
