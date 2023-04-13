from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    """
    Thread Model
    participants = [value1, value2] - ONLY 2 values
    """
    participants = models.ManyToManyField(User, related_name='threads', verbose_name='Participant')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'Thread {self.id}'


class Message(models.Model):
    """
    Message Model
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
