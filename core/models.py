from django.db import models

class Conversation(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=10, default="en")
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone


class Message(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:30]}"
