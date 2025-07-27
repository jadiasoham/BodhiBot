from django.db import models
from users.models import User

class Chat(models.Model):
    # user = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    user = models.CharField(max_length= 50, verbose_name= "user name", default= "Anonymous User", help_text= "Identifier for the user, can be a username or any unique identifier, is extracted from the decoded jwt token sent from the frontend.")
    name = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add= True)
    last_message = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"Chat started at {self.created_at}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name= "chat_messages", on_delete= models.CASCADE)
    sender = models.CharField(max_length= 50)
    content = models.TextField(verbose_name= "message")
    timestamp = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Message: {self.content} sent by {self.sender} at {self.timestamp}"
