from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Thread, Message


class UserSerializer(serializers.ModelSerializer):
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


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'thread', 'sender', 'is_read', 'created')

    def create(self, validated_data):
        thread = validated_data['thread']
        if validated_data['sender'] not in thread.participants.all():
            raise serializers.ValidationError("You're not the member of this thread")
        validated_data['thread'] = thread
        return super(MessageSerializer, self).create(validated_data)

        # user = User.objects.get(pk=validated_data['id'])
        # message = Message.objects.create(
        #     text=validated_data['text'],
        #     thread=validated_data['thread'],
        #     sender=user,
        #     is_read=validated_data['is_read']
        # )
        # message.save()
        # return message


class ThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ('id', 'participants', 'created', 'updated', 'last_message')

    def create(self, validated_data):
        valid_participants = validated_data.get('participants')
        print(valid_participants)
        print(type(valid_participants))
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
