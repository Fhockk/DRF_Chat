from django.contrib import admin

from chat.models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants_list')

    def participants_list(self, obj):
        return ", ".join([str(user) for user in obj.participants.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread_id', 'sender', 'text', 'created', 'is_read')
    list_filter = ('thread__id', 'sender', 'is_read')
    search_fields = ('text', 'sender__username')

